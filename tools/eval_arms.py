"""Model client and arm runners for the equal-cost bar.

Transport: OpenRouter's OpenAI-compatible API. Models, temperature and seed
are always explicit — the shared inference floor depends on it.
"""

import os
import time

from eval_scoring import deterministic_verdict

OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"
DEFAULT_ARM_MODEL = "deepseek/deepseek-v4.1-flash"
DEFAULT_JUDGE_MODEL = "meta/muse-spark-1.3-contributor"


class BudgetExceeded(Exception):
    """Raised when an arm's output tokens exceed the item budget."""


class ChatClient:
    """Thin wrapper over OpenRouter. Reads OPENROUTER_API_KEY at construction."""

    def __init__(self):
        api_key = os.environ.get("OPENROUTER_API_KEY")
        if not api_key:
            raise RuntimeError("OPENROUTER_API_KEY is not set")
        from openai import OpenAI

        self._client = OpenAI(base_url=OPENROUTER_BASE_URL, api_key=api_key)

    def complete(self, system, user, model, temperature, max_tokens, seed=7, reasoning=None):
        started = time.time()
        extra = {"reasoning": {"effort": "none"}} if reasoning == "none" else None
        response = self._client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
            temperature=temperature,
            max_tokens=max_tokens,
            seed=seed,
            extra_body=extra,
        )
        latency = time.time() - started
        usage = response.usage
        text = (response.choices[0].message.content or "").strip()
        return {
            "text": text,
            "output_tokens": int(getattr(usage, "completion_tokens", 0) or 0),
            "input_tokens": int(getattr(usage, "prompt_tokens", 0) or 0),
            "latency_s": round(latency, 3),
        }


def _check_budget(total_tokens, budget):
    if total_tokens > budget:
        raise BudgetExceeded(f"arm used {total_tokens} output tokens > budget {budget}")


def run_without(client, item, chart, ledger_entry, budget, doctrine_prompt):
    """Three independent samples, deterministic filter, best survivor wins."""
    share = budget // 3
    samples = []
    total = 0
    for _ in range(3):
        out = client.complete(
            system=doctrine_prompt,
            user=_user_prompt(item, chart),
            model=item.get("model", DEFAULT_ARM_MODEL),
            temperature=0.7,
            max_tokens=share,
            reasoning="none",
        )
        total += out["output_tokens"]
        _check_budget(total, budget)
        verdict = deterministic_verdict(out["text"], ledger_entry, chart)
        samples.append((len(verdict["failures"]), out, verdict))

    samples.sort(key=lambda s: s[0])
    best = samples[0]
    return {
        "text": best[1]["text"],
        "output_tokens": total,
        "latency_s": sum(s[1]["latency_s"] for s in samples),
        "disqualified": False,
        "samples": 3,
        "deterministic": best[2],
    }


def _user_prompt(item, chart):
    import json

    return (
        f"Chart data (computed):\n{json.dumps(chart, sort_keys=True)}\n\n"
        f"Question:\n{item['prompt']}"
    )


def _agent_prompt(name):
    """Read a shipped agent definition from agents/."""
    import pathlib

    path = pathlib.Path(__file__).resolve().parent.parent / "agents" / name
    if not path.is_file():
        raise RuntimeError(f"missing agent definition: {path}")
    return path.read_text(encoding="utf-8")


def _prompt_file(name):
    """Read an eval prompt from evals/prompts/."""
    import pathlib

    path = pathlib.Path(__file__).resolve().parent.parent / "evals" / "prompts" / name
    if not path.is_file():
        raise RuntimeError(f"missing eval prompt: {path}")
    return path.read_text(encoding="utf-8")


def _agent_model(item):
    return item.get("model", DEFAULT_ARM_MODEL)


def run_bare(client, item, chart, budget, bare_prompt=None):
    """Single completion, no doctrine, whole budget."""
    system = bare_prompt or _prompt_file("bare_system.md")
    out = client.complete(
        system=system,
        user=_user_prompt(item, chart),
        model=_agent_model(item),
        temperature=0,
        max_tokens=budget,
        reasoning="none",
    )
    _check_budget(out["output_tokens"], budget)
    return {
        "text": out["text"],
        "output_tokens": out["output_tokens"],
        "latency_s": out["latency_s"],
        "disqualified": False,
        "samples": 1,
    }


def _revision_prompt(draft, verifier_text, critic_text):
    """Carry only deny/nonconformant lines into the revision request."""
    lines = []
    for block in (verifier_text, critic_text):
        for line in block.splitlines():
            lowered = line.lower()
            if "deny" in lowered or "nonconformant" in lowered or "unsupported" in lowered:
                lines.append(line.strip())
    findings = "\n".join(lines) if lines else "none"
    return (
        f"Your draft:\n{draft}\n\n"
        f"Verifier/critic findings that must be applied:\n{findings}\n\n"
        "Rewrite the answer applying only these findings. Do not add new claims. "
        "Keep every grounded claim that was not denied."
    )


def run_with(client, item, chart, ledger_entry, budget, doctrine_prompt):
    """Draft (B/3) -> chart-verifier (B/6) -> doctrine-critic (B/6) -> revision (B/3)."""
    model = _agent_model(item)
    user = _user_prompt(item, chart)
    total = 0

    draft = client.complete(
        system=doctrine_prompt, user=user, model=model, temperature=0, max_tokens=budget // 3,
        reasoning="none",
    )
    total += draft["output_tokens"]
    _check_budget(total, budget)

    verifier = client.complete(
        system=_agent_prompt("chart-verifier.md"),
        user=user + "\n\nDraft to verify:\n" + draft["text"],
        model=model,
        temperature=0,
        max_tokens=budget // 6,
        reasoning="none",
    )
    total += verifier["output_tokens"]
    _check_budget(total, budget)

    critic = client.complete(
        system=_agent_prompt("doctrine-critic.md"),
        user=user + "\n\nDraft to critique:\n" + draft["text"],
        model=model,
        temperature=0,
        max_tokens=budget // 6,
        reasoning="none",
    )
    total += critic["output_tokens"]
    _check_budget(total, budget)

    revision = client.complete(
        system=doctrine_prompt,
        user=_revision_prompt(draft["text"], verifier["text"], critic["text"]),
        model=model,
        temperature=0,
        max_tokens=budget // 3,
        reasoning="none",
    )
    total += revision["output_tokens"]
    _check_budget(total, budget)

    return {
        "text": revision["text"],
        "output_tokens": total,
        "latency_s": draft["latency_s"] + verifier["latency_s"] + critic["latency_s"] + revision["latency_s"],
        "disqualified": False,
        "samples": 1,
        "stages": {
            "draft": draft["text"],
            "verifier": verifier["text"],
            "critic": critic["text"],
        },
    }
