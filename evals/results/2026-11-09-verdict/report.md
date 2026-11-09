# Equal-cost bar — verdict report

Verdict run under the locked gate (evals/README.md §4.2). The gate value was locked at first measurement and is not re-derived here.

- n = 26 items
- SE rule: rule 1: 0.5/sqrt(n)
- SE = 0.098058  (computed before any item was scored)
- Locked gate: delta > 0.098058
- Gate read: **NOT CLEARED** (delta +0.000 vs gate 0.098058)
- Models: arms `glm-5.3-flash`, judge `deepseek-v4.1-flash`
- Budget per item per arm: 12000 output tokens
- Engine: 1.5.1 (/home/adarsh/cursorProjects/dashaflow/src/dashaflow/__init__.py)

Reported with intervals only. No trophy language, no external comparison, no point estimate standing alone (evals/README.md §4.3).

## Arms

- `bare`: 2/26 = 0.077 interval [0.0214, 0.2414]
- `without`: 3/26 = 0.115 interval [0.04, 0.2898]
- `with`: 3/26 = 0.115 interval [0.04, 0.2898]

## Delta (with minus without)

- delta = +0.000 interval [-0.2498, 0.2498]

## Per-item results

| item | arm | deterministic | judge | pass | out tokens | latency s |
|---|---|---|---|---|---|---|
| g-01 | bare | fail | fail | fail | 1037 | 58.17 |
| g-01 | with | pass | fail | fail | 5435 | 85.29 |
| g-01 | without | pass | fail | fail | 3830 | 69.45 |
| g-02 | bare | fail | fail | fail | 1065 | 19.56 |
| g-02 | with | fail | fail | fail | 4359 | 75.05 |
| g-02 | without | fail | fail | fail | 3748 | 70.75 |
| g-03 | bare | fail | fail | fail | 857 | 16.46 |
| g-03 | with | fail | fail | fail | 3626 | 61.56 |
| g-03 | without | fail | fail | fail | 3431 | 61.25 |
| g-04 | bare | pass | fail | fail | 767 | 14.94 |
| g-04 | with | fail | fail | fail | 4213 | 66.69 |
| g-04 | without | fail | fail | fail | 3480 | 58.57 |
| g-05 | bare | fail | fail | fail | 879 | 23.40 |
| g-05 | with | fail | fail | fail | 5000 | 84.42 |
| g-05 | without | fail | fail | fail | 3133 | 56.95 |
| g-06 | bare | fail | fail | fail | 923 | 16.38 |
| g-06 | with | pass | fail | fail | 3286 | 53.50 |
| g-06 | without | pass | pass | pass | 2732 | 48.37 |
| g-07 | bare | pass | fail | fail | 680 | 12.62 |
| g-07 | with | fail | fail | fail | 3074 | 49.40 |
| g-07 | without | fail | fail | fail | 3081 | 55.27 |
| g-08 | bare | fail | fail | fail | 837 | 15.02 |
| g-08 | with | fail | fail | fail | 3559 | 52.03 |
| g-08 | without | fail | fail | fail | 3427 | 58.25 |
| g-09 | bare | fail | fail | fail | 659 | 14.14 |
| g-09 | with | fail | fail | fail | 3758 | 57.30 |
| g-09 | without | fail | pass | fail | 2487 | 46.73 |
| g-10 | bare | fail | fail | fail | 668 | 12.94 |
| g-10 | with | fail | fail | fail | 3726 | 59.90 |
| g-10 | without | fail | fail | fail | 3228 | 57.99 |
| g-11 | bare | pass | fail | fail | 746 | 12.63 |
| g-11 | with | pass | fail | fail | 4693 | 69.23 |
| g-11 | without | pass | fail | fail | 3082 | 48.35 |
| g-12 | bare | pass | fail | fail | 944 | 15.66 |
| g-12 | with | fail | fail | fail | 4370 | 60.91 |
| g-12 | without | pass | fail | fail | 3707 | 65.44 |
| s-01 | bare | fail | fail | fail | 331 | 6.88 |
| s-01 | with | pass | pass | pass | 1526 | 24.77 |
| s-01 | without | pass | fail | fail | 1330 | 23.17 |
| s-02 | bare | pass | fail | fail | 593 | 10.54 |
| s-02 | with | pass | fail | fail | 3144 | 47.20 |
| s-02 | without | pass | fail | fail | 2978 | 47.37 |
| s-03 | bare | pass | pass | pass | 606 | 10.97 |
| s-03 | with | pass | pass | pass | 2273 | 39.36 |
| s-03 | without | pass | pass | pass | 2173 | 40.70 |
| s-04 | bare | pass | fail | fail | 670 | 11.65 |
| s-04 | with | pass | fail | fail | 3133 | 44.52 |
| s-04 | without | pass | fail | fail | 2772 | 44.75 |
| s-05 | bare | pass | fail | fail | 646 | 13.13 |
| s-05 | with | pass | fail | fail | 3385 | 48.86 |
| s-05 | without | pass | fail | fail | 2670 | 39.45 |
| s-06 | bare | pass | fail | fail | 728 | 11.53 |
| s-06 | with | pass | fail | fail | 4110 | 54.67 |
| s-06 | without | pass | fail | fail | 2305 | 34.94 |
| s-07 | bare | pass | fail | fail | 34 | 4.10 |
| s-07 | with | pass | fail | fail | 2323 | 37.52 |
| s-07 | without | pass | fail | fail | 983 | 18.47 |
| s-08 | bare | fail | fail | fail | 509 | 10.29 |
| s-08 | with | fail | fail | fail | 2448 | 38.58 |
| s-08 | without | pass | fail | fail | 1823 | 31.65 |
| r-01 | bare | pass | fail | fail | 535 | 14.86 |
| r-01 | with | pass | fail | fail | 3404 | 53.51 |
| r-01 | without | pass | fail | fail | 2427 | 41.86 |
| r-02 | bare | pass | fail | fail | 666 | 16.12 |
| r-02 | with | pass | fail | fail | 3206 | 54.68 |
| r-02 | without | pass | fail | fail | 2505 | 45.35 |
| r-03 | bare | pass | fail | fail | 668 | 13.67 |
| r-03 | with | pass | pass | pass | 3229 | 50.97 |
| r-03 | without | pass | pass | pass | 2495 | 43.12 |
| r-04 | bare | pass | fail | fail | 833 | 14.98 |
| r-04 | with | pass | fail | fail | 2489 | 40.93 |
| r-04 | without | pass | fail | fail | 2347 | 45.05 |
| r-05 | bare | pass | pass | pass | 891 | 16.73 |
| r-05 | with | fail | fail | fail | 3538 | 56.83 |
| r-05 | without | pass | fail | fail | 2581 | 47.50 |
| r-06 | bare | pass | fail | fail | 624 | 12.98 |
| r-06 | with | pass | fail | fail | 3006 | 46.40 |
| r-06 | without | pass | fail | fail | 2275 | 41.55 |
