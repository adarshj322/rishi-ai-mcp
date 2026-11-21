"""Zero-human conformance screen: chart-fact checks and chart-swap.

This measures grounding and chart-sensitivity only. It is not reading quality
and it is not expert validation. See evals/zero-human/README.md.
"""

import argparse
import datetime
import json
import pathlib
import sys

from eval_arms import ChatClient, run_without
from eval_runner import (
    _engine_provenance,
    judge_response,
    load_jsonl,
    load_ledger,
    load_prompt,
    precompute_chart,
)
from eval_scoring import extract_numeric_claims, find_fabrications


def shift_birth(birth: dict, hours: int = 12) -> dict:
    """Return a copy of the birth data with the time shifted by `hours`."""
    t = datetime.time.fromisoformat(birth["time"])
    shifted = (
        datetime.datetime.combine(datetime.date.min, t) + datetime.timedelta(hours=hours)
    ).time()
    out = dict(birth)
    out["time"] = shifted.strftime("%H:%M")
    return out


def chart_text_divergence(
    real_text: str, decoy_text: str, real_chart: dict, decoy_chart: dict | None = None
) -> dict:
    """Compare a real-chart reading with a decoy-chart reading.

    A1 is the real reading's fabrication list against the real chart. A2 passes
    only when both readings assert at least one numeric chart claim, the two
    claim sets share less than half their values, and — when the decoy chart is
    supplied — the decoy reading fits its own chart. Identical texts always
    fail: a chart-blind pipeline cannot distinguish the charts.
    """
    real_fab = find_fabrications(real_text, real_chart)
    decoy_fab = find_fabrications(decoy_text, decoy_chart or real_chart)
    real_claims = {c.lower() for c in extract_numeric_claims(real_text)}
    decoy_claims = {c.lower() for c in extract_numeric_claims(decoy_text)}
    union = real_claims | decoy_claims
    overlap = 1.0 if not union else len(real_claims & decoy_claims) / len(union)
    exercised = bool(real_claims) and bool(decoy_claims)
    fits_own_chart = decoy_chart is None or not decoy_fab
    return {
        "real_fabrications": real_fab,
        "decoy_fabrications": decoy_fab,
        "real_claims_checked": len(real_claims),
        "claim_overlap": overlap,
        "exercised": exercised,
        "pass": exercised and overlap < 0.5 and fits_own_chart,
    }


def parse_judge_models(spec):
    """Parse `model`, `model:effort` entries into (models, efforts)."""
    models = []
    efforts = {}
    for entry in spec.split(","):
        entry = entry.strip()
        if not entry:
            continue
        if ":" in entry:
            model, effort = entry.rsplit(":", 1)
        else:
            model, effort = entry, None
        model = model.strip()
        effort = effort.strip() if effort else None
        if model:
            models.append(model)
            if effort:
                efforts[model] = effort
    return models, efforts


def judge_consistency(judge_client, item, entry, chart, text, judge_models, trials,
                      judge_reasoning=None):
    """Repeat a clause judge across models and trials; report agreement only.

    Agreement is consistency, not quality: judges can agree on the same wrong
    verdict. No validity claim is made here.
    """
    verdicts = []
    errors = 0
    for model in judge_models:
        for _ in range(trials):
            judged = judge_response(
                judge_client, item, entry, chart, text, judge_model=model,
                reasoning=(judge_reasoning or {}).get(model),
            )
            errors += int(judged["judge_error"])
            verdicts.append((model, judged["pass"], judged["clauses"]))

    def agreement_for(group):
        pairs = 0
        same = 0
        for i in range(len(group)):
            for j in range(i + 1, len(group)):
                pairs += 1
                same += int(group[i] == group[j])
        return (same / pairs) if pairs else 1.0

    by_model = {}
    for model in judge_models:
        group = [v[1] for v in verdicts if v[0] == model]
        by_model[model] = {"pass": sum(group), "n": len(group),
                          "agreement": agreement_for(group)}

    positions = {}
    for _, _, clauses in verdicts:
        for index, clause in enumerate(clauses):
            positions.setdefault(index, []).append(clause.get("verdict"))
    clause_pairs = 0
    clause_same = 0
    for group in positions.values():
        clause_pairs += len(group) * (len(group) - 1) // 2
        clause_same += sum(
            1 for i in range(len(group)) for j in range(i + 1, len(group))
            if group[i] == group[j]
        )
    clause_agreement = (clause_same / clause_pairs) if clause_pairs else 1.0

    passes = [v[1] for v in verdicts]
    pairwise = agreement_for(passes)
    return {
        "per_model": by_model,
        "pairwise_agreement": pairwise,
        "clause_agreement": clause_agreement,
        "judge_errors": errors,
        "pass": pairwise >= 0.8 and errors == 0,
    }


def cast_decoy(item):
    """Cast the time-shifted decoy, keeping any transit block the item names."""
    return precompute_chart(dict(item, birth=shift_birth(item["birth"])))


def screen_item(item, entry, client, doctrine_prompt, arm_model, budget, reasoning="none"):
    """Run A1/A2 for one item and return both texts plus their checks."""
    chart = precompute_chart(item)
    decoy_chart = cast_decoy(item)
    run_item = dict(item, model=arm_model)
    real = run_without(
        client, run_item, chart, entry, budget, doctrine_prompt, reasoning=reasoning
    )
    decoy = run_without(
        client, run_item, decoy_chart, entry, budget, doctrine_prompt, reasoning=reasoning
    )
    divergence = chart_text_divergence(
        real["text"], decoy["text"], chart, decoy_chart
    )
    claims_checked = divergence["real_claims_checked"]
    return {
        "a1": {
            "pass": not divergence["real_fabrications"] and claims_checked > 0,
            "fabrications": divergence["real_fabrications"],
            "claims_checked": claims_checked,
            "exercised": claims_checked > 0,
        },
        "a2": divergence,
        "real_text": real["text"],
        "decoy_text": decoy["text"],
        "tokens": real["output_tokens"] + decoy["output_tokens"],
    }


BOUNDARY = (
    "chart-grounded, rule-faithful, internally consistent — "
    "not validated against expert judgment"
)


def write_report(payload, outdir):
    """Write the human-readable report; the boundary sentence is mandatory."""
    summary = payload.get("summary", {})

    def cell(key):
        passed, n = summary.get(key, [0, 0])
        return "not run" if n == 0 else f"{passed}/{n}"

    lines = [
        "# Zero-human conformance screen",
        "",
        f"**Claim boundary:** {BOUNDARY}.",
        "",
        "| Check | Pass |",
        "|---|---|",
        f"| A1 chart-fact | {cell('a1')} |",
        f"| A2 chart-swap | {cell('a2')} |",
        f"| A4 judge consistency | {cell('a4')} |",
        "",
        f"Arm output tokens: {summary.get('tokens', 0)}",
        "",
        "## Per item",
        "",
        "| Item | A1 | Claims | Fabrications | A2 | Claim overlap | A4 agreement | A4 clauses |",
        "|---|---|---|---|---|---|---|---|",
    ]
    for result in payload.get("items", []):
        a1 = result.get("a1", {})
        a2 = result.get("a2", {})
        a4 = result.get("a4")
        fab = ", ".join(a1.get("fabrications", [])) or "—"
        if not a1.get("exercised", True):
            a1_status = "not exercised"
        else:
            a1_status = "pass" if a1.get("pass") else "fail"
        a4_agreement = "not run" if a4 is None else format(a4.get("pairwise_agreement", 0), ".2f")
        a4_clauses = "not run" if a4 is None else format(a4.get("clause_agreement", 0), ".2f")
        lines.append(
            f"| {result.get('id', '?')} | {a1_status} | {a1.get('claims_checked', 0)} | {fab} "
            f"| {'pass' if a2.get('pass') else 'fail'} "
            f"| {a2.get('claim_overlap', 0):.2f} "
            f"| {a4_agreement} | {a4_clauses} |"
        )
    lines.extend(
        [
            "",
            "## Limits",
            "",
            "- A1 checks degree and date claims only. Sign and house claims are not checked.",
            "- A1 counts a reading as pass only when it asserted at least one numeric claim; "
            "zero claims read as not exercised.",
            "- A2 shows chart sensitivity, not chart truth.",
            "- A4 measures agreement among judges. A panel can agree on the same wrong verdict.",
            "- Nothing here measures reading quality or correspondence to the person.",
        ]
    )
    config = payload.get("config")
    if config:
        lines.extend(["", "## Provenance", ""])
        for key in (
            "generated_at",
            "transport",
            "arm_model",
            "arm_reasoning",
            "judge_models",
            "judge_reasoning",
            "trials",
            "budget",
            "items",
            "engine",
        ):
            if key in config:
                value = config[key]
                if isinstance(value, list):
                    value = ", ".join(str(v) for v in value)
                elif isinstance(value, dict):
                    value = json.dumps(value, sort_keys=True)
                lines.append(f"- {key}: {value}")
    lines.append("")
    pathlib.Path(outdir, "report.md").write_text("\n".join(lines), encoding="utf-8")


def main(argv=None):
    parser = argparse.ArgumentParser(description="Zero-human conformance screen (A1/A2).")
    parser.add_argument("--cases", default="evals/v2/cases")
    parser.add_argument("--items", default="grounding.jsonl")
    parser.add_argument("--limit", type=int, default=0)
    parser.add_argument("--out", default="/tmp/zero-human")
    parser.add_argument("--transport", default="openrouter")
    parser.add_argument("--arm-model", default=None)
    parser.add_argument("--judge-models", default="")
    parser.add_argument("--trials", type=int, default=3)
    parser.add_argument("--budget", type=int, default=700)
    parser.add_argument("--arm-reasoning", default="none")
    args = parser.parse_args(argv)

    items = load_jsonl(args.items, protocol="v2")
    if args.limit:
        items = items[: args.limit]
    ledger = load_ledger(protocol="v2")
    doctrine = load_prompt("doctrine_system.md")
    client = ChatClient(transport=args.transport)
    arm_model = args.arm_model or {
        "openrouter": "deepseek/deepseek-v4.1-flash",
        "opencode-go": "deepseek-v4.1-flash",
    }[args.transport]

    results = []
    judge_models, judge_reasoning = parse_judge_models(args.judge_models)
    for item in items:
        entry = ledger[item["id"]]
        result = screen_item(
            item,
            entry,
            client,
            doctrine,
            arm_model,
            args.budget,
            reasoning=None if args.arm_reasoning == "default" else args.arm_reasoning,
        )
        if judge_models:
            result["a4"] = judge_consistency(
                client,
                item,
                entry,
                precompute_chart(item),
                result["real_text"],
                judge_models,
                args.trials,
                judge_reasoning=judge_reasoning,
            )
        results.append({"id": item["id"], **result})
        print(f"[{len(results)}/{len(items)}] {item['id']}", flush=True)

    outdir = pathlib.Path(args.out)
    outdir.mkdir(parents=True, exist_ok=True)
    payload = {
        "config": {
            "generated_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
            "transport": args.transport,
            "arm_model": arm_model,
            "arm_reasoning": args.arm_reasoning,
            "judge_models": judge_models,
            "judge_reasoning": judge_reasoning,
            "trials": args.trials,
            "budget": args.budget,
            "items": args.items,
            "engine": _engine_provenance(),
        },
        "items": results,
        "summary": {
            "a1": [sum(r["a1"]["pass"] for r in results), len(results)],
            "a2": [sum(r["a2"]["pass"] for r in results), len(results)],
            "a4": [
                sum(r["a4"]["pass"] for r in results if "a4" in r),
                sum(1 for r in results if "a4" in r),
            ],
            "tokens": sum(r.get("tokens", 0) for r in results),
        },
    }
    (outdir / "results.json").write_text(json.dumps(payload, indent=1), encoding="utf-8")
    write_report(payload, str(outdir))
    print(outdir / "report.md")
    return 0


if __name__ == "__main__":
    sys.exit(main())
