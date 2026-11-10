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

- delta = +0.000 interval [-0.1154, 0.1154]

## Per-item results

| item | arm | deterministic | judge | pass | out tokens | latency s |
|---|---|---|---|---|---|---|
| g-01 | bare | fail | fail | fail | 859 | 13.05 |
| g-01 | without | pass | fail | fail | 3515 | 44.94 |
| g-01 | with | fail | fail | fail | 6362 | 74.06 |
| g-02 | bare | fail | fail | fail | 1053 | 15.05 |
| g-02 | without | fail | fail | fail | 4082 | 53.36 |
| g-02 | with | fail | fail | fail | 4013 | 50.06 |
| g-03 | bare | fail | fail | fail | 640 | 9.27 |
| g-03 | without | pass | fail | fail | 3030 | 38.53 |
| g-03 | with | pass | fail | fail | 4546 | 55.16 |
| g-04 | bare | pass | fail | fail | 822 | 14.65 |
| g-04 | without | pass | fail | fail | 3306 | 42.60 |
| g-04 | with | pass | fail | fail | 3788 | 47.37 |
| g-05 | bare | fail | fail | fail | 803 | 12.19 |
| g-05 | without | fail | fail | fail | 3117 | 43.30 |
| g-05 | with | fail | fail | fail | 4730 | 60.63 |
| g-06 | bare | pass | fail | fail | 831 | 12.28 |
| g-06 | without | pass | fail | fail | 2772 | 39.00 |
| g-06 | with | pass | fail | fail | 2720 | 35.98 |
| g-07 | bare | fail | fail | fail | 721 | 11.14 |
| g-07 | without | pass | fail | fail | 2637 | 35.69 |
| g-07 | with | pass | fail | fail | 3098 | 41.26 |
| g-08 | bare | pass | fail | fail | 791 | 11.79 |
| g-08 | without | pass | fail | fail | 2843 | 41.79 |
| g-08 | with | pass | fail | fail | 3654 | 47.39 |
| g-09 | bare | fail | fail | fail | 755 | 11.29 |
| g-09 | without | pass | pass | pass | 2632 | 37.88 |
| g-09 | with | fail | fail | fail | 3554 | 46.95 |
| g-10 | bare | fail | fail | fail | 719 | 11.28 |
| g-10 | without | fail | fail | fail | 3135 | 44.94 |
| g-10 | with | fail | fail | fail | 3671 | 46.65 |
| g-11 | bare | pass | fail | fail | 756 | 10.61 |
| g-11 | without | pass | fail | fail | 2631 | 37.84 |
| g-11 | with | pass | fail | fail | 3914 | 51.38 |
| g-12 | bare | pass | fail | fail | 707 | 10.28 |
| g-12 | without | pass | fail | fail | 3277 | 48.26 |
| g-12 | with | pass | fail | fail | 4677 | 60.54 |
| s-01 | bare | pass | fail | fail | 290 | 5.56 |
| s-01 | without | pass | fail | fail | 1686 | 25.13 |
| s-01 | with | pass | pass | pass | 2286 | 34.90 |
| s-02 | bare | pass | fail | fail | 659 | 10.31 |
| s-02 | without | pass | fail | fail | 2781 | 39.55 |
| s-02 | with | pass | fail | fail | 3543 | 46.92 |
| s-03 | bare | pass | pass | pass | 525 | 8.31 |
| s-03 | without | pass | pass | pass | 2394 | 36.63 |
| s-03 | with | pass | pass | pass | 2606 | 37.34 |
| s-04 | bare | pass | fail | fail | 782 | 12.15 |
| s-04 | without | pass | fail | fail | 2778 | 41.14 |
| s-04 | with | pass | fail | fail | 3261 | 44.23 |
| s-05 | bare | pass | fail | fail | 635 | 10.23 |
| s-05 | without | pass | fail | fail | 2401 | 34.65 |
| s-05 | with | pass | fail | fail | 3144 | 43.29 |
| s-06 | bare | pass | fail | fail | 564 | 9.17 |
| s-06 | without | pass | fail | fail | 2395 | 38.12 |
| s-06 | with | pass | fail | fail | 2376 | 36.38 |
| s-07 | bare | pass | fail | fail | 60 | 2.81 |
| s-07 | without | pass | fail | fail | 1029 | 18.98 |
| s-07 | with | pass | fail | fail | 1717 | 27.38 |
| s-08 | bare | pass | fail | fail | 459 | 7.69 |
| s-08 | without | pass | fail | fail | 1673 | 25.05 |
| s-08 | with | pass | fail | fail | 2197 | 36.07 |
| r-01 | bare | pass | fail | fail | 617 | 9.61 |
| r-01 | without | pass | fail | fail | 2281 | 34.26 |
| r-01 | with | pass | fail | fail | 3977 | 53.92 |
| r-02 | bare | pass | fail | fail | 674 | 11.49 |
| r-02 | without | pass | fail | fail | 2615 | 40.07 |
| r-02 | with | pass | fail | fail | 3159 | 45.99 |
| r-03 | bare | pass | pass | pass | 750 | 12.47 |
| r-03 | without | pass | pass | pass | 2486 | 35.97 |
| r-03 | with | pass | pass | pass | 3641 | 51.70 |
| r-04 | bare | pass | fail | fail | 876 | 14.13 |
| r-04 | without | pass | fail | fail | 2796 | 43.89 |
| r-04 | with | pass | fail | fail | 2659 | 39.60 |
| r-05 | bare | pass | fail | fail | 634 | 11.68 |
| r-05 | without | pass | fail | fail | 2405 | 35.25 |
| r-05 | with | pass | fail | fail | 3612 | 50.35 |
| r-06 | bare | pass | fail | fail | 549 | 9.82 |
| r-06 | without | pass | fail | fail | 2401 | 37.83 |
| r-06 | with | pass | fail | fail | 3284 | 45.33 |
