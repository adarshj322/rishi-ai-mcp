# Equal-cost bar — verdict report

Verdict run under the locked gate (evals/README.md §4.2). The gate value was locked at first measurement and is not re-derived here.

- n = 40 items
- SE rule: rule 1: 0.5/sqrt(n)
- SE = 0.079057  (computed before any item was scored)
- Locked gate: delta > 0.079057
- Gate read: **CLEARED** (delta +0.100 vs gate 0.079057)
- Models: arms `glm-5.3-flash`, judge `deepseek-v4.1-flash`
- Budget per item per arm: 12000 output tokens
- Engine: 1.5.1 (/home/adarsh/cursorProjects/dashaflow/src/dashaflow/__init__.py)

Reported with intervals only. No trophy language, no external comparison, no point estimate standing alone (evals/README.md §4.3).

## Arms

- `bare`: 16/40 = 0.400 interval [0.2635, 0.554]
- `shipped`: 20/40 = 0.500 interval [0.352, 0.648]

## Delta (with minus without)

- delta = +0.100 interval [-0.025, 0.225]

## Per-item results

| item | arm | deterministic | judge | pass | out tokens | latency s |
|---|---|---|---|---|---|---|
| v2-g-01 | bare | pass | fail | fail | 2693 | 21.25 |
| v2-g-01 | shipped | pass | fail | fail | 3724 | 42.98 |
| v2-g-02 | bare | pass | pass | pass | 730 | 15.31 |
| v2-g-02 | shipped | pass | pass | pass | 3495 | 58.16 |
| v2-g-03 | bare | pass | fail | fail | 911 | 16.55 |
| v2-g-03 | shipped | pass | fail | fail | 3183 | 54.13 |
| v2-g-04 | bare | pass | fail | fail | 861 | 15.35 |
| v2-g-04 | shipped | pass | fail | fail | 3678 | 63.10 |
| v2-g-05 | bare | fail | fail | fail | 836 | 24.06 |
| v2-g-05 | shipped | fail | pass | fail | 3222 | 68.79 |
| v2-g-06 | bare | fail | fail | fail | 808 | 15.62 |
| v2-g-06 | shipped | fail | pass | fail | 2985 | 56.94 |
| v2-g-07 | bare | pass | fail | fail | 812 | 19.61 |
| v2-g-07 | shipped | pass | fail | fail | 2596 | 50.71 |
| v2-g-08 | bare | pass | fail | fail | 744 | 20.73 |
| v2-g-08 | shipped | pass | fail | fail | 2905 | 63.78 |
| v2-g-09 | bare | pass | pass | pass | 727 | 13.39 |
| v2-g-09 | shipped | pass | fail | fail | 3497 | 50.61 |
| v2-g-10 | bare | pass | pass | pass | 700 | 12.18 |
| v2-g-10 | shipped | pass | pass | pass | 2787 | 46.11 |
| v2-g-11 | bare | pass | pass | pass | 576 | 10.87 |
| v2-g-11 | shipped | pass | fail | fail | 2306 | 37.17 |
| v2-g-12 | bare | pass | pass | pass | 538 | 10.87 |
| v2-g-12 | shipped | pass | pass | pass | 2547 | 38.67 |
| v2-g-13 | bare | pass | pass | pass | 530 | 9.18 |
| v2-g-13 | shipped | pass | pass | pass | 1729 | 29.09 |
| v2-g-14 | bare | pass | pass | pass | 427 | 7.51 |
| v2-g-14 | shipped | pass | pass | pass | 1599 | 27.26 |
| v2-g-15 | bare | pass | pass | pass | 608 | 9.60 |
| v2-g-15 | shipped | pass | pass | pass | 2489 | 46.39 |
| v2-g-16 | bare | pass | pass | pass | 818 | 13.78 |
| v2-g-16 | shipped | pass | pass | pass | 2778 | 42.61 |
| v2-g-17 | bare | fail | pass | fail | 912 | 13.87 |
| v2-g-17 | shipped | pass | pass | pass | 2839 | 45.02 |
| v2-g-18 | bare | pass | fail | fail | 830 | 13.76 |
| v2-g-18 | shipped | pass | pass | pass | 2946 | 46.27 |
| v2-g-19 | bare | fail | fail | fail | 764 | 13.71 |
| v2-g-19 | shipped | fail | fail | fail | 2658 | 53.69 |
| v2-g-20 | bare | pass | fail | fail | 608 | 11.05 |
| v2-g-20 | shipped | pass | fail | fail | 2460 | 38.54 |
| v2-s-01 | bare | pass | pass | pass | 532 | 8.83 |
| v2-s-01 | shipped | pass | pass | pass | 2437 | 37.77 |
| v2-s-02 | bare | pass | fail | fail | 509 | 10.74 |
| v2-s-02 | shipped | pass | fail | fail | 2526 | 42.28 |
| v2-s-03 | bare | pass | pass | pass | 651 | 11.68 |
| v2-s-03 | shipped | pass | pass | pass | 2940 | 45.59 |
| v2-s-04 | bare | pass | pass | pass | 644 | 10.48 |
| v2-s-04 | shipped | pass | pass | pass | 2889 | 53.38 |
| v2-s-05 | bare | pass | fail | fail | 643 | 13.38 |
| v2-s-05 | shipped | pass | pass | pass | 3020 | 48.40 |
| v2-s-06 | bare | pass | pass | pass | 652 | 11.22 |
| v2-s-06 | shipped | pass | pass | pass | 2967 | 53.69 |
| v2-s-07 | bare | pass | fail | fail | 583 | 10.04 |
| v2-s-07 | shipped | pass | pass | pass | 2435 | 40.02 |
| v2-s-08 | bare | pass | pass | pass | 540 | 9.47 |
| v2-s-08 | shipped | pass | pass | pass | 2483 | 39.72 |
| v2-s-09 | bare | pass | fail | fail | 617 | 11.33 |
| v2-s-09 | shipped | pass | fail | fail | 2452 | 38.09 |
| v2-s-10 | bare | pass | fail | fail | 602 | 10.81 |
| v2-s-10 | shipped | pass | fail | fail | 2592 | 42.01 |
| v2-r-01 | bare | pass | fail | fail | 617 | 10.52 |
| v2-r-01 | shipped | pass | fail | fail | 2019 | 32.74 |
| v2-r-02 | bare | pass | fail | fail | 580 | 10.58 |
| v2-r-02 | shipped | pass | fail | fail | 2866 | 46.05 |
| v2-r-03 | bare | pass | pass | pass | 693 | 11.63 |
| v2-r-03 | shipped | pass | pass | pass | 2525 | 51.92 |
| v2-r-04 | bare | pass | pass | pass | 695 | 12.21 |
| v2-r-04 | shipped | pass | pass | pass | 2509 | 43.78 |
| v2-r-05 | bare | pass | fail | fail | 629 | 12.22 |
| v2-r-05 | shipped | pass | pass | pass | 2490 | 42.64 |
| v2-r-06 | bare | pass | fail | fail | 890 | 16.59 |
| v2-r-06 | shipped | pass | fail | fail | 2132 | 35.23 |
| v2-r-07 | bare | pass | fail | fail | 781 | 14.17 |
| v2-r-07 | shipped | pass | fail | fail | 2538 | 40.23 |
| v2-r-08 | bare | pass | fail | fail | 944 | 14.85 |
| v2-r-08 | shipped | pass | fail | fail | 3201 | 52.76 |
| v2-r-09 | bare | pass | fail | fail | 792 | 12.76 |
| v2-r-09 | shipped | pass | fail | fail | 2618 | 43.53 |
| v2-r-10 | bare | pass | fail | fail | 781 | 12.96 |
| v2-r-10 | shipped | pass | pass | pass | 2505 | 48.35 |
