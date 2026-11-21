"""Public exam competence screen (A3).

Scores a model on keyed multiple-choice questions from public exams. This tests
shastra recall, not chart interpretation or reading quality.
"""

import argparse
import json
import pathlib
import re
import sys

from eval_arms import ChatClient


def score_exam(client, questions, model, budget, max_tokens=64):
    """Answer each question and compare the first A-D letter to the key."""
    correct = 0
    errors = []
    used = 0
    for q in questions:
        options = "\n".join(f"{letter}. {text}" for letter, text in sorted(q["options"].items()))
        out = client.complete(
            system=(
                "Answer the multiple-choice question with one letter (A, B, C or D). "
                "Reply with the letter only."
            ),
            user=f"{q['question']}\n\n{options}",
            model=model,
            temperature=0,
            max_tokens=max_tokens,
        )
        used += out["output_tokens"]
        if used > budget:
            raise RuntimeError(f"exam exceeded output budget {budget}")
        match = re.search(r"\b([A-D])\b", out["text"].upper())
        got = match.group(1) if match else None
        ok = got == q["answer"]
        correct += int(ok)
        if not ok:
            errors.append({"id": q["id"], "expected": q["answer"], "got": got})
    n = len(questions)
    return {
        "correct": correct,
        "n": n,
        "accuracy": correct / n if n else 0.0,
        "errors": errors,
        "output_tokens": used,
    }


def main(argv=None):
    parser = argparse.ArgumentParser(description="Public exam competence screen (A3).")
    parser.add_argument("--questions", required=True, help="JSONL with id/question/options/answer")
    parser.add_argument("--out", default=None)
    parser.add_argument("--transport", default="openrouter")
    parser.add_argument("--model", default=None)
    parser.add_argument("--budget", type=int, default=4000)
    args = parser.parse_args(argv)

    with open(args.questions, encoding="utf-8") as fh:
        questions = [json.loads(line) for line in fh if line.strip()]
    model = args.model or {
        "openrouter": "deepseek/deepseek-v4.1-flash",
        "opencode-go": "deepseek-v4.1-flash",
    }[args.transport]
    result = score_exam(ChatClient(transport=args.transport), questions, model, args.budget)
    result["provenance"] = {"source": args.questions, "model": model}
    text = json.dumps(result, indent=1)
    if args.out:
        pathlib.Path(args.out).write_text(text, encoding="utf-8")
    print(text)


if __name__ == "__main__":
    sys.exit(main())
