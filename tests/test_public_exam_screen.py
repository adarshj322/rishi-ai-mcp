import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "tools"))

from public_exam_screen import score_exam


def test_score_exam_marks_correct_and_wrong():
    questions = [
        {"id": "q1", "question": "2+2?", "options": {"A": "4", "B": "5"}, "answer": "A"},
        {"id": "q2", "question": "3+3?", "options": {"A": "5", "B": "6"}, "answer": "B"},
    ]

    class C:
        def complete(self, *a, **k):
            return {"text": "A", "output_tokens": 1, "input_tokens": 1, "latency_s": 0.0}

    result = score_exam(C(), questions, "m", 100)
    assert result["correct"] == 1 and result["n"] == 2 and result["accuracy"] == 0.5
