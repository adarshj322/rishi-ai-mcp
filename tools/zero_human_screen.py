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
from eval_runner import load_jsonl, load_ledger, load_prompt, precompute_chart
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


def chart_text_divergence(real_text: str, decoy_text: str, real_chart: dict) -> dict:
    """Compare a real-chart reading with a decoy-chart reading.

    A1 is the real reading's fabrication list against the real chart. A2 passes
    when the decoy reading makes more fabricated claims than the real one, or
    when the two readings share fewer than half of their numeric claims. Identical
    texts always fail: a chart-blind pipeline cannot distinguish the charts.
    """
    real_fab = find_fabrications(real_text, real_chart)
    decoy_fab = find_fabrications(decoy_text, real_chart)
    real_claims = {c.lower() for c in extract_numeric_claims(real_text)}
    decoy_claims = {c.lower() for c in extract_numeric_claims(decoy_text)}
    union = real_claims | decoy_claims
    overlap = 1.0 if not union else len(real_claims & decoy_claims) / len(union)
    return {
        "real_fabrications": real_fab,
        "decoy_fabrications": decoy_fab,
        "claim_overlap": overlap,
        "pass": len(decoy_fab) > len(real_fab) or overlap < 0.5,
    }


def _cast(birth):
    import dashaflow

    return dashaflow.cast_chart(
        birth["dob"], birth["time"], birth["lat"], birth["lon"], birth["tz"]
    )


def screen_item(item, entry, client, doctrine_prompt, arm_model, budget, reasoning="none"):
    """Run A1/A2 for one item and return both texts plus their checks."""
    chart = precompute_chart(item)
    decoy_chart = _cast(shift_birth(item["birth"]))
    run_item = dict(item, model=arm_model)
    real = run_without(
        client, run_item, chart, entry, budget, doctrine_prompt, reasoning=reasoning
    )
    decoy = run_without(
        client, run_item, decoy_chart, entry, budget, doctrine_prompt, reasoning=reasoning
    )
    divergence = chart_text_divergence(real["text"], decoy["text"], chart)
    return {
        "a1": {
            "pass": not divergence["real_fabrications"],
            "fabrications": divergence["real_fabrications"],
        },
        "a2": divergence,
        "real_text": real["text"],
        "decoy_text": decoy["text"],
        "tokens": real["output_tokens"] + decoy["output_tokens"],
    }


def main(argv=None):
    parser = argparse.ArgumentParser(description="Zero-human conformance screen (A1/A2).")
    parser.add_argument("--cases", default="evals/v2/cases")
    parser.add_argument("--items", default="grounding.jsonl")
    parser.add_argument("--limit", type=int, default=0)
    parser.add_argument("--out", default="/tmp/zero-human")
    parser.add_argument("--transport", default="openrouter")
    parser.add_argument("--arm-model", default=None)
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
    for item in items:
        result = screen_item(
            item,
            ledger["items"][item["id"]],
            client,
            doctrine,
            arm_model,
            args.budget,
            reasoning=None if args.arm_reasoning == "default" else args.arm_reasoning,
        )
        results.append({"id": item["id"], **result})
        print(f"[{len(results)}/{len(items)}] {item['id']}", flush=True)

    outdir = pathlib.Path(args.out)
    outdir.mkdir(parents=True, exist_ok=True)
    payload = {
        "items": results,
        "summary": {
            "a1": [sum(r["a1"]["pass"] for r in results), len(results)],
            "a2": [sum(r["a2"]["pass"] for r in results), len(results)],
        },
    }
    (outdir / "results.json").write_text(json.dumps(payload, indent=1), encoding="utf-8")
    write_report(payload, str(outdir))
    print(outdir / "report.md")


if __name__ == "__main__":
    sys.exit(main())
