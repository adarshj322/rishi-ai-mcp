# Public exam screen (A3)

Scores a model on keyed multiple-choice questions from public exams. It tests
**shastra recall** — terminology and rule recognition — not chart interpretation,
not whole-reading quality, and not expert agreement.

## Question format

One JSON object per line:

```json
{"id": "baziqa-001", "question": "...", "options": {"A": "...", "B": "...", "C": "...", "D": "..."}, "answer": "B"}
```

## Sources

- **BaziQA** — 555 expert-authored questions over 117 real charts, keys and
  champion scores in its public repo. Design analogue only: Chinese BaZi, not
  Vedic content.
- **CUET-PG Jyotish (Falit)** — NTA papers with official keys. Sanskrit-medium
  shastra recall. Transcribe carefully; a wrong key silently corrupts the score,
  so keep `errors` per item and spot-check against the official PDF.

## Run

```bash
python tools/public_exam_screen.py --questions evals/zero-human/public_exam/baziqa.jsonl
```

Report `accuracy` with its n. A high score means the model knows the vocabulary;
it says nothing about whether a reading is good.
