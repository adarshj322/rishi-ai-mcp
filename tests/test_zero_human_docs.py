import pathlib


def test_zero_human_boundary_and_inventory():
    root = pathlib.Path(__file__).resolve().parents[1]
    readme = (root / "evals" / "zero-human" / "README.md").read_text()
    assert "chart-grounded, rule-faithful, internally consistent — not validated against expert judgment" in readme
    assert "A1" in readme and "A2" in readme and "A4" in readme
    resources = (root / "evals" / "zero-human" / "public_resources.md").read_text()
    for name in ("OurNakshatra", "Jyotish-LLM", "BaziQA", "CUET-PG", "BPHS"):
        assert name in resources
    assert "not validated" in readme
