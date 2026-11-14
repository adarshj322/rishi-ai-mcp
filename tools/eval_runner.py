"""Equal-cost bar runner — orchestration, judge, and interval-enforcing report.

Usage:
  python tools/eval_runner.py --mode pilot [--arms bare,without,with] \
      [--budget 3000] [--items g-01,...] [--out evals/results/<date>-pilot]
"""

import argparse
import datetime
import json
import os
import pathlib
import random
import re
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from eval_arms import (  # noqa: E402
    ChatClient,
    models_for_transport,
    run_bare,
    run_with,
    run_without,
)
from eval_scoring import (  # noqa: E402
    compute_se,
    deterministic_verdict,
    wilson_interval,
)

ROOT = pathlib.Path(__file__).resolve().parent.parent
CASES = ROOT / "evals" / "cases"
PROMPTS = ROOT / "evals" / "prompts"
PROTOCOLS = {
    "v1": {
        "cases": CASES,
        "gate": ROOT / "evals" / "locked_gate.json",
        "files": ("grounding.jsonl", "sycophancy.jsonl", "remedy.jsonl"),
        "gate_arms": ("with", "without"),
        "default_arms": ("bare", "without", "with"),
    },
    "v2": {
        "cases": ROOT / "evals" / "v2" / "cases",
        "gate": ROOT / "evals" / "v2" / "locked_gate.json",
        "files": ("grounding.jsonl", "sycophancy.jsonl", "remedy.jsonl"),
        "gate_arms": ("shipped", "bare"),
        "default_arms": ("bare", "shipped"),
    },
}


def _protocol_paths(protocol):
    if protocol not in PROTOCOLS:
        raise ValueError(f"unknown protocol: {protocol}")
    return PROTOCOLS[protocol]

ARM_LABEL_RE = re.compile(
    r"^\s*(?:answer\s*)?\((?:with|without|bare)(?:\s+arm)?\)\s*:?\s*", re.I
)
ARM_WORD_RE = re.compile(r"\b(?:arm|bare|without|with)\b", re.I)


def anonymize(text):
    """Strip arm labels and leading answer-prefix artifacts."""
    cleaned = ARM_LABEL_RE.sub("", text)
    cleaned = re.sub(r"^\s*Answer\s*:\s*", "", cleaned, flags=re.I)
    return cleaned.strip()


def load_jsonl(name, protocol="v1"):
    records = []
    with open(_protocol_paths(protocol)["cases"] / name, encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if line:
                records.append(json.loads(line))
    return records


def load_ledger(protocol="v1"):
    with open(_protocol_paths(protocol)["cases"] / "ledger.json", encoding="utf-8") as fh:
        return json.load(fh)["items"]


def load_prompt(name):
    return (PROMPTS / name).read_text(encoding="utf-8")


def _extract_json(text):
    """Parse the judge's JSON, tolerating fences and surrounding prose.

    Tries: direct parse, fenced block, then each balanced object candidate
    from the end of the text (the verdict is the last thing emitted).
    """
    candidate = text.strip()
    if candidate.startswith("```"):
        candidate = re.sub(r"^```(?:json)?\s*|\s*```$", "", candidate, flags=re.S)
    try:
        return json.loads(candidate)
    except json.JSONDecodeError:
        pass
    starts = [i for i, ch in enumerate(candidate) if ch == "{"]
    for start in reversed(starts):
        depth = 0
        for end in range(start, len(candidate)):
            if candidate[end] == "{":
                depth += 1
            elif candidate[end] == "}":
                depth -= 1
                if depth == 0:
                    try:
                        return json.loads(candidate[start: end + 1])
                    except json.JSONDecodeError:
                        break
    raise ValueError("no JSON object found")


def judge_response(client, item, ledger_entry, chart, response_text, judge_model):
    """Reference-guided, anonymized, clause-by-clause judging. One retry on parse failure."""
    system = load_prompt("judge.md")
    payload = {
        "chart": chart,
        "clauses": [c["text"] for c in ledger_entry.get("clauses", [])],
        "response": anonymize(response_text),
    }
    user = json.dumps(payload, sort_keys=True)
    last_error = None
    for _ in range(2):
        out = client.complete(
            system=system, user=user, model=judge_model, temperature=0, max_tokens=16000
        )
        try:
            parsed = _extract_json(out["text"])
            clauses = parsed.get("clauses", [])
            expected = len(ledger_entry.get("clauses", []))
            # One verdict per mandatory clause; an empty/partial list is a
            # judge failure, never a silent free pass.
            if expected and len(clauses) != expected:
                raise ValueError(f"judge returned {len(clauses)} clause verdicts, expected {expected}")
            passed = parsed.get("overall") == "pass" and all(
                c.get("verdict") == "pass" for c in clauses
            )
            return {
                "pass": passed,
                "clauses": clauses,
                "judge_error": False,
                "output_tokens": out["output_tokens"],
            }
        except (ValueError, json.JSONDecodeError) as exc:  # retry once
            last_error = exc
    return {"pass": False, "clauses": [], "judge_error": True, "output_tokens": 0,
            "error": str(last_error)}


def precompute_chart(item):
    """Cast the item's chart (and transit, when the item names a date) once."""
    import dashaflow

    birth = item["birth"]
    chart = dashaflow.cast_chart(
        birth["dob"], birth["time"], birth["lat"], birth["lon"], birth["tz"]
    )
    if item.get("transit_date"):
        chart["transit"] = dashaflow.cast_transit(
            item["transit_date"], birth["dob"], birth["time"],
            birth["lat"], birth["lon"], birth["tz"],
        )
    return chart


def _resolve_models(transport, arm_model=None, judge_model=None):
    """Transport defaults, overridable per run; overrides are recorded in results."""
    transport_arm, transport_judge = models_for_transport(transport)
    return arm_model or transport_arm, judge_model or transport_judge


def run(items, arms, budget, outdir, client=None, judge_client=None, transport="openrouter",
        arm_model=None, judge_model=None, arm_reasoning="none", mode="pilot",
        resume=False, protocol="v1"):
    """Execute the three-arm comparison and return the results dict."""
    client = client or ChatClient(transport=transport)
    judge_client = judge_client or client
    arm_model, judge_model = _resolve_models(transport, arm_model, judge_model)
    reasoning = None if arm_reasoning == "default" else arm_reasoning
    for item in items:
        item.setdefault("model", arm_model)
    config = {
        "protocol": protocol,
        "mode": mode,
        "item_ids": [item["id"] for item in items],
        "transport": transport,
        "arm_model": arm_model,
        "judge_model": judge_model,
        "arm_reasoning": arm_reasoning,
        "budget": budget,
        "arms": sorted(arms),
        "engine": _engine_provenance(),
        "scoring_hash": _scoring_hash(protocol),
    }
    completed = _resume_state(outdir, config) if resume else {}
    if completed:
        print(f"resuming: {len(completed)}/{len(items)} items from partial.json", flush=True)
    ledger = load_ledger(protocol)
    doctrine_prompt = load_prompt("doctrine_system.md")
    bare_prompt = load_prompt("bare_system.md")
    se = compute_se(len(items))
    if mode == "verdict":
        _assert_verdict_ready(items, config, protocol)

    item_results = [completed[item["id"]] for item in items if item["id"] in completed]
    charts = {}
    total = len(items)
    for item in items:
        if item["id"] in completed:
            charts[item["id"]] = precompute_chart(item)
    for item in items:
        if item["id"] in completed:
            continue
        entry = ledger[item["id"]]
        chart = precompute_chart(item)
        charts[item["id"]] = chart
        arm_results = {}
        for arm in arms:
            try:
                if arm == "bare":
                    out = run_bare(client, item, chart, budget, bare_prompt=bare_prompt,
                                   reasoning=reasoning)
                elif arm == "without":
                    if protocol == "v2":
                        raise ValueError("v2 uses the 'shipped' arm, not 'without'")
                    out = run_without(client, item, chart, entry, budget, doctrine_prompt,
                                      reasoning=reasoning)
                elif arm == "shipped":
                    if protocol != "v2":
                        raise ValueError("'shipped' is a v2 arm")
                    out = run_without(client, item, chart, entry, budget, doctrine_prompt,
                                      reasoning=reasoning)
                elif arm == "with":
                    if protocol != "v1":
                        raise ValueError("v2 has no verification arm")
                    out = run_with(client, item, chart, entry, budget, doctrine_prompt,
                                   reasoning=reasoning)
                else:
                    raise ValueError(f"unknown arm: {arm}")
            except Exception as exc:
                if exc.__class__.__name__ == "BudgetExceeded":
                    out = {"disqualified": True, "text": "", "output_tokens": budget + 1,
                           "latency_s": 0.0}
                else:
                    raise
            det = deterministic_verdict(out["text"], entry, chart)
            judged = judge_response(
                judge_client, item, entry, chart, out["text"],
                judge_model=judge_model,
            )
            arm_results[arm] = {
                "text": out["text"],
                "output_tokens": out["output_tokens"],
                "latency_s": out.get("latency_s", 0.0),
                "disqualified": out.get("disqualified", False),
                "deterministic": det,
                "judge": judged,
                "pass": (not out.get("disqualified")) and det["pass"] and judged["pass"],
                "judge_error": judged["judge_error"],
            }
        item_results.append({"id": item["id"], "arms": arm_results})
        _write_partial(outdir, item_results, total, len(item_results), config)
        print(f"[{len(item_results)}/{total}] {item['id']}", flush=True)

    summary = tally(item_results, arms)
    valid = _run_valid(summary)
    delta = _delta(item_results, summary, arms, protocol)
    results = {
        "mode": mode,
        "protocol": protocol,
        "resumed": bool(completed),
        "resume_from": len(completed),
        "valid": valid,
        "locked_gate": _locked_gate(),
        "items": item_results,
        "arms": summary,
        "se": se,
        "se_rule": "rule 1: 0.5/sqrt(n)",
        "gate": f"delta > {se:.6f}",
        "delta": delta,
        "engines": _engine_provenance(),
        "models": {"arm": arm_model, "judge": judge_model, "transport": transport,
                   "arm_reasoning": arm_reasoning},
        "budget": budget,
        "generated_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
    }
    os.makedirs(outdir, exist_ok=True)
    with open(os.path.join(outdir, "charts.json"), "w", encoding="utf-8") as fh:
        json.dump(charts, fh, sort_keys=True)
    _write_manifest(outdir, results, [item["id"] for item in items])
    write_report(results, outdir)
    try:
        os.remove(os.path.join(outdir, "partial.json"))
    except FileNotFoundError:
        pass
    return results


def _write_partial(outdir, item_results, total, done, config):
    """Persist finished items + the run config atomically for a safe resume."""
    os.makedirs(outdir, exist_ok=True)
    path = os.path.join(outdir, "partial.json")
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as fh:
        json.dump(
            {"config": config, "done": done, "total": total, "items": item_results},
            fh,
        )
    os.replace(tmp, path)


def _resume_state(outdir, config):
    """Return completed items if the checkpoint matches this exact run; else {}."""
    path = os.path.join(outdir, "partial.json")
    if not os.path.exists(path):
        return {}
    with open(path, encoding="utf-8") as fh:
        payload = json.load(fh)
    if payload.get("config") != config:
        raise ValueError(
            "partial.json belongs to a different run (mode/floor/corpus/instrument); "
            "refusing to resume"
        )
    return {item["id"]: item for item in payload.get("items", [])}


def _scoring_hash(protocol="v1"):
    """Hash the scoring rules, prompts, and selected corpus — not the orchestrator."""
    import hashlib

    cases = _protocol_paths(protocol)["cases"]
    paths = [
        ROOT / "tools" / "eval_scoring.py",
        PROMPTS / "bare_system.md",
        PROMPTS / "doctrine_system.md",
        PROMPTS / "judge.md",
        ROOT / "evals" / "agents" / "chart-verifier.md",
        ROOT / "evals" / "agents" / "doctrine-critic.md",
        cases / "ledger.json",
        cases / "grounding.jsonl",
        cases / "sycophancy.jsonl",
        cases / "remedy.jsonl",
    ]
    digest = hashlib.sha256()
    for path in paths:
        if not path.is_file():
            raise RuntimeError(f"required scoring input missing: {path}")
        digest.update(path.read_bytes())
    return digest.hexdigest()


def _engine_provenance():
    import dashaflow

    return {
        "dashaflow_version": getattr(dashaflow, "__version__", "unknown"),
        "dashaflow_file": getattr(dashaflow, "__file__", "unknown"),
    }


def tally(item_results, arms):
    """Per-arm pass counts with intervals; judge-error items excluded from both arms."""
    excluded = [
        it["id"] for it in item_results
        if any(it["arms"].get(a, {}).get("judge_error") for a in arms)
    ]
    out = {"excluded": excluded}
    for arm in arms:
        entries = [it["arms"].get(arm, {}) for it in item_results if it["id"] not in excluded]
        if any(e.get("disqualified") for e in entries):
            out[arm] = {"disqualified": True, "reason": "budget overrun"}
            continue
        n = len(entries)
        passes = sum(1 for e in entries if e.get("pass"))
        low, high = wilson_interval(passes, n) if n else (0.0, 0.0)
        out[arm] = {
            "passes": passes,
            "n": n,
            "proportion": (passes / n) if n else 0.0,
            "interval": [round(low, 4), round(high, 4)],
        }
    return out


LOCKED_GATE_PATH = ROOT / "evals" / "locked_gate.json"


def _locked_gate(protocol="v1"):
    with open(_protocol_paths(protocol)["gate"], encoding="utf-8") as fh:
        return json.load(fh)


def _assert_verdict_ready(items, config, protocol="v1"):
    """A verdict needs the full corpus, the locked gate, and the recorded floor."""
    locked = _locked_gate(protocol)
    if len(items) != locked["n"]:
        raise ValueError(
            f"verdict mode requires the locked corpus of {locked['n']} items; got {len(items)}"
        )
    se = compute_se(len(items))
    if abs(se - locked["se"]) > 1e-5:
        raise ValueError(f"computed SE {se} does not match locked SE {locked['se']}")
    for key, expected in locked.get("floor_config", {}).items():
        if config.get(key) != expected:
            raise ValueError(
                f"verdict floor mismatch on {key}: {config.get(key)!r} != {expected!r}"
            )


def _repo_commit():
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True
        ).strip()
    except (OSError, subprocess.CalledProcessError):
        return "unknown"


def _prompt_hashes():
    import hashlib

    paths = [
        PROMPTS / "bare_system.md",
        PROMPTS / "doctrine_system.md",
        PROMPTS / "judge.md",
        ROOT / "evals" / "agents" / "chart-verifier.md",
        ROOT / "evals" / "agents" / "doctrine-critic.md",
    ]
    hashes = {}
    for path in paths:
        if not path.is_file():
            raise RuntimeError(f"required prompt missing: {path}")
        hashes[str(path.relative_to(ROOT))] = hashlib.sha256(path.read_bytes()).hexdigest()
    return hashes


def _write_manifest(outdir, results, item_ids):
    os.makedirs(outdir, exist_ok=True)
    payload = {
        "repo_commit": _repo_commit(),
        "generated_at": results.get("generated_at"),
        "mode": results.get("mode"),
        "protocol": results.get("protocol"),
        "resumed": results.get("resumed"),
        "resume_from": results.get("resume_from"),
        "transport": results.get("models", {}).get("transport"),
        "models": results.get("models"),
        "budget": results.get("budget"),
        "item_ids": item_ids,
        "prompt_hashes": _prompt_hashes(),
        "engine": results.get("engines"),
    }
    with open(os.path.join(outdir, "manifest.json"), "w", encoding="utf-8") as fh:
        json.dump(payload, fh, indent=1, sort_keys=True)


def _paired_delta_interval(item_results, arms, resamples=2000, seed=12345):
    """Paired bootstrap over items; returns a 95% interval for with-minus-without."""
    pairs = []
    for item in item_results:
        if any(item["arms"].get(arm, {}).get("judge_error") for arm in arms):
            continue
        with_arm = item["arms"].get("with", {})
        without_arm = item["arms"].get("without", {})
        pairs.append(
            (1.0 if with_arm.get("pass") else 0.0,
             1.0 if without_arm.get("pass") else 0.0)
        )
    if not pairs:
        return [0.0, 0.0]
    rng = random.Random(seed)
    n = len(pairs)
    deltas = []
    for _ in range(resamples):
        with_sum = without_sum = 0.0
        for _ in range(n):
            with_pass, without_pass = pairs[rng.randrange(n)]
            with_sum += with_pass
            without_sum += without_pass
        deltas.append((with_sum - without_sum) / n)
    deltas.sort()
    return [round(deltas[int(0.025 * resamples)], 4),
            round(deltas[int(0.975 * resamples) - 1], 4)]


def _run_valid(summary):
    """A run is valid only if no item was excluded and no arm was disqualified."""
    if summary.get("excluded"):
        return False
    return not any(
        stats.get("disqualified")
        for arm, stats in summary.items()
        if arm != "excluded"
    )


def _delta(item_results, summary, arms, protocol="v1"):
    gate_arms = _protocol_paths(protocol)["gate_arms"]
    if any(arm not in arms for arm in gate_arms):
        return {"value": None, "interval": None, "note": "gate arms not both run"}
    a, b = summary.get(gate_arms[0], {}), summary.get(gate_arms[1], {})
    if "proportion" not in a or "proportion" not in b:
        return {"value": None, "interval": None, "note": "an arm was disqualified"}
    return {
        "value": round(a["proportion"] - b["proportion"], 4),
        "interval": _paired_delta_interval(item_results, list(gate_arms)),
    }


def write_report(results, outdir):
    """Write report.md. Every proportion carries an interval; SE precedes scoring."""
    for arm, stats in results["arms"].items():
        if arm == "excluded":
            continue
        if "proportion" in stats and "interval" not in stats:
            raise AssertionError(f"arm {arm} has a proportion without an interval")

    mode = results.get("mode", "pilot")
    delta = results.get("delta") or {}
    valid = results.get("valid", True)
    gate_cleared = None
    if mode == "verdict" and delta.get("value") is not None and valid:
        gate_cleared = delta["value"] > results["se"]
        results["gate_cleared"] = gate_cleared

    if mode == "verdict":
        title = "# Equal-cost bar — verdict report"
        intro = (
            "Verdict run under the locked gate (evals/README.md §4.2). The gate "
            "value was locked at first measurement and is not re-derived here."
        )
    else:
        title = "# Equal-cost bar — pilot report"
        intro = (
            "Pilot run: the noise floor only. No verdict is taken from this run "
            "(evals/README.md §4.2(d))."
        )

    lines = [
        title,
        "",
        intro,
        "",
        f"- n = {len(results['items'])} items",
        f"- SE rule: {results.get('se_rule', 'rule 1')}",
        f"- SE = {results['se']:.6f}  (computed before any item was scored)",
        f"- Locked gate: {results['gate']}",
        *(
            ["- Gate read: **INVALID — excluded items; no verdict**"]
            if mode == "verdict" and not valid
            else [f"- Gate read: **{'CLEARED' if gate_cleared else 'NOT CLEARED'}** "
                  f"(delta {delta['value']:+.3f} vs gate {results['se']:.6f})"]
            if mode == "verdict" and delta.get("value") is not None
            else []
        ),
        f"- Models: arms `{results.get('models', {}).get('arm', 'unknown')}`, "
        f"judge `{results.get('models', {}).get('judge', 'unknown')}`",
        f"- Budget per item per arm: {results.get('budget', 'unknown')} output tokens",
        f"- Engine: {results.get('engines', {}).get('dashaflow_version', 'unknown')} "
        f"({results.get('engines', {}).get('dashaflow_file', 'unknown')})",
        "",
        "Reported with intervals only. No trophy language, no external comparison, "
        "no point estimate standing alone (evals/README.md §4.3).",
        "",
        "## Arms",
        "",
    ]
    for arm in ("bare", "shipped", "without", "with"):
        if arm not in results["arms"]:
            continue
        stats = results["arms"][arm]
        if stats.get("disqualified"):
            lines.append(f"- `{arm}`: DISQUALIFIED ({stats.get('reason')}) — no proportion printed")
        elif "proportion" in stats:
            lines.append(
                f"- `{arm}`: {stats['passes']}/{stats['n']} = {stats['proportion']:.3f} "
                f"interval [{stats['interval'][0]}, {stats['interval'][1]}]"
            )
    lines += ["", "## Delta (with minus without)", ""]
    delta = results.get("delta") or {}
    if delta.get("value") is None:
        lines.append(f"No delta: {delta.get('note', 'unavailable')}")
    else:
        lines.append(f"- delta = {delta['value']:+.3f} interval [{delta['interval'][0]}, {delta['interval'][1]}]")
    if results["arms"].get("excluded"):
        lines += ["", "## Excluded items (judge error — excluded from both arms)", ""]
        lines += [f"- {item_id}" for item_id in results["arms"]["excluded"]]
    lines += ["", "## Per-item results", "",
              "| item | arm | deterministic | judge | pass | out tokens | latency s |",
              "|---|---|---|---|---|---|---|"]
    for item in results["items"]:
        for arm, r in item["arms"].items():
            if r.get("disqualified"):
                lines.append(f"| {item['id']} | {arm} | DISQUALIFIED | — | — | {r['output_tokens']} | — |")
                continue
            judge = "error" if r["judge_error"] else ("pass" if r["judge"]["pass"] else "fail")
            det = "pass" if r["deterministic"]["pass"] else "fail"
            lines.append(
                f"| {item['id']} | {arm} | {det} | {judge} | {'pass' if r['pass'] else 'fail'} "
                f"| {r['output_tokens']} | {r['latency_s']:.2f} |"
            )
    path = os.path.join(outdir, "report.md")
    with open(path, "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines) + "\n")
    with open(os.path.join(outdir, "results.json"), "w", encoding="utf-8") as fh:
        json.dump(results, fh, indent=1, sort_keys=True)
    return path


def build_items(selected_ids=None, protocol="v1"):
    items = []
    for name in _protocol_paths(protocol)["files"]:
        for record in load_jsonl(name, protocol):
            if selected_ids and record["id"] not in selected_ids:
                continue
            items.append(record)
    return items


def main(argv=None):
    parser = argparse.ArgumentParser(description="Equal-cost bar runner")
    parser.add_argument("--mode", default="pilot", choices=["pilot", "verdict", "dry-run"])
    parser.add_argument("--protocol", default="v1", choices=["v1", "v2"])
    parser.add_argument("--arms", default="")
    parser.add_argument("--budget", type=int, default=6000)
    parser.add_argument("--items", default="")
    parser.add_argument("--transport", default="openrouter", choices=["openrouter", "opencode-go"])
    parser.add_argument("--arm-model", default="")
    parser.add_argument("--judge-model", default="")
    parser.add_argument("--arm-reasoning", default="none", choices=["default", "none"])
    parser.add_argument("--resume", action="store_true")
    parser.add_argument("--out", default="")
    args = parser.parse_args(argv)

    arms = [a.strip() for a in args.arms.split(",") if a.strip()]
    if not arms:
        arms = list(_protocol_paths(args.protocol)["default_arms"])
    selected = [i.strip() for i in args.items.split(",") if i.strip()] or None
    items = build_items(selected, args.protocol)
    outdir = args.out or f"evals/results/{datetime.date.today().isoformat()}-pilot"
    results = run(
        items, arms, args.budget, outdir, transport=args.transport,
        arm_model=args.arm_model or None, judge_model=args.judge_model or None,
        arm_reasoning=args.arm_reasoning, mode=args.mode, resume=args.resume,
        protocol=args.protocol,
    )
    print(f"SE = {results['se']:.6f} (rule 1); gate: {results['gate']}")
    for arm in ("bare", "shipped", "without", "with"):
        stats = results["arms"].get(arm)
        if not stats:
            continue
        if stats.get("disqualified"):
            print(f"{arm}: DISQUALIFIED ({stats.get('reason')})")
        else:
            print(f"{arm}: {stats['passes']}/{stats['n']} = {stats['proportion']:.3f} "
                  f"[{stats['interval'][0]}, {stats['interval'][1]}]")
    print(f"report: {os.path.join(outdir, 'report.md')}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
