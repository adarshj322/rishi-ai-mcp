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

    def complete(self, system, user, model, temperature, max_tokens, seed=7):
        started = time.time()
        response = self._client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
            temperature=temperature,
            max_tokens=max_tokens,
            seed=seed,
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
