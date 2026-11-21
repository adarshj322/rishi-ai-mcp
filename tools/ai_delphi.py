"""AI Delphi rubric pre-pass (A5).

Persona panels propose rubric items and report panel disagreement. It cannot
measure dissent fidelity against a human panel: without humans there is no
minority vote to compare, so only panel disagreement is reported.
"""

import argparse
import json
import re
import sys

from eval_arms import ChatClient


def _normalize(text):
    return re.sub(r"\s+", " ", text.strip().lower()).rstrip(" .;:")


def run_delphi(client, topic, personas, rounds, model, budget, max_tokens=400):
    """Collect rubric items from each persona/round and count mentions."""
    counts = {}
    used = 0
    for persona in personas:
        for _ in range(rounds):
            out = client.complete(
                system=f"You are {persona}. Propose evaluation rubric items.",
                user=(
                    f"Topic: {topic}\n"
                    "List five short rubric items, one per line, each starting with '- '. "
                    "No preamble."
                ),
                model=model,
                temperature=0.7,
                max_tokens=max_tokens,
            )
            used += out["output_tokens"]
            if used > budget:
                raise RuntimeError(f"delphi exceeded output budget {budget}")
            for line in out["text"].splitlines():
                line = line.strip()
                if line.startswith("- "):
                    item = _normalize(line[2:])
                    if item:
                        counts[item] = counts.get(item, 0) + 1

    items = [
        {"text": text, "mentions": mentions}
        for text, mentions in sorted(counts.items(), key=lambda kv: (-kv[1], kv[0]))
    ]
    total = sum(counts.values())
    disagreement = 1.0 - (max(counts.values()) / total) if total else 0.0
    return {
        "items": items,
        "panel_disagreement": disagreement,
        "output_tokens": used,
    }


def main(argv=None):
    parser = argparse.ArgumentParser(description="AI Delphi rubric pre-pass (A5).")
    parser.add_argument("--topic", required=True)
    parser.add_argument("--personas", required=True, help="comma-separated persona names")
    parser.add_argument("--rounds", type=int, default=1)
    parser.add_argument("--transport", default="openrouter")
    parser.add_argument("--model", default=None)
    parser.add_argument("--budget", type=int, default=4000)
    args = parser.parse_args(argv)

    model = args.model or {
        "openrouter": "deepseek/deepseek-v4.1-flash",
        "opencode-go": "deepseek-v4.1-flash",
    }[args.transport]
    result = run_delphi(
        ChatClient(transport=args.transport),
        args.topic,
        [p.strip() for p in args.personas.split(",") if p.strip()],
        args.rounds,
        model,
        args.budget,
    )
    print(json.dumps(result, indent=1))


if __name__ == "__main__":
    sys.exit(main())
