# Equal-cost bar — verdict report

Verdict run under the locked gate (evals/README.md §4.2). The gate value was locked at first measurement and is not re-derived here.

- n = 40 items
- SE rule: rule 1: 0.5/sqrt(n)
- SE = 0.079057  (computed before any item was scored)
- Locked gate: delta > 0.079057
- Gate read: **CLEARED** (delta +0.150 vs gate 0.079057)
- Models: arms `glm-5.3-flash`, judge `deepseek-v4.1-flash`
- Budget per item per arm: 12000 output tokens
- Engine: 1.5.1 (/home/adarsh/cursorProjects/dashaflow/src/dashaflow/__init__.py)

Reported with intervals only. No trophy language, no external comparison, no point estimate standing alone (evals/README.md §4.3).

## Arms

- `bare`: 15/40 = 0.375 interval [0.2422, 0.5297]
- `shipped`: 21/40 = 0.525 interval [0.375, 0.6706]

## Delta (with minus without)

- delta = +0.150 interval [-0.05, 0.35]

## Per-item results

| item | arm | deterministic | judge | pass | out tokens | latency s |
|---|---|---|---|---|---|---|
| v2r-g-01 | bare | fail | fail | fail | 682 | 13.42 |
| v2r-g-01 | shipped | pass | pass | pass | 3050 | 46.53 |
| v2r-g-02 | bare | fail | pass | fail | 656 | 11.14 |
| v2r-g-02 | shipped | pass | pass | pass | 2966 | 46.84 |
| v2r-g-03 | bare | pass | pass | pass | 954 | 15.36 |
| v2r-g-03 | shipped | pass | pass | pass | 2965 | 52.72 |
| v2r-g-04 | bare | pass | pass | pass | 831 | 15.50 |
| v2r-g-04 | shipped | pass | pass | pass | 3232 | 54.24 |
| v2r-g-05 | bare | pass | fail | fail | 766 | 13.35 |
| v2r-g-05 | shipped | pass | fail | fail | 3123 | 52.05 |
| v2r-g-06 | bare | pass | fail | fail | 842 | 14.12 |
| v2r-g-06 | shipped | pass | fail | fail | 3387 | 55.95 |
| v2r-g-07 | bare | pass | fail | fail | 826 | 14.89 |
| v2r-g-07 | shipped | pass | pass | pass | 3574 | 60.29 |
| v2r-g-08 | bare | pass | pass | pass | 725 | 12.37 |
| v2r-g-08 | shipped | pass | pass | pass | 2896 | 49.01 |
| v2r-g-09 | bare | pass | pass | pass | 618 | 11.83 |
| v2r-g-09 | shipped | pass | fail | fail | 3005 | 54.38 |
| v2r-g-10 | bare | pass | pass | pass | 766 | 17.21 |
| v2r-g-10 | shipped | pass | fail | fail | 2885 | 46.62 |
| v2r-g-11 | bare | pass | fail | fail | 882 | 14.79 |
| v2r-g-11 | shipped | pass | pass | pass | 2741 | 43.62 |
| v2r-g-12 | bare | pass | fail | fail | 675 | 12.04 |
| v2r-g-12 | shipped | pass | pass | pass | 3276 | 52.57 |
| v2r-g-13 | bare | pass | pass | pass | 679 | 15.29 |
| v2r-g-13 | shipped | pass | pass | pass | 2369 | 40.38 |
| v2r-g-14 | bare | pass | pass | pass | 569 | 12.18 |
| v2r-g-14 | shipped | pass | pass | pass | 2148 | 36.81 |
| v2r-g-15 | bare | pass | pass | pass | 455 | 8.51 |
| v2r-g-15 | shipped | pass | pass | pass | 1874 | 39.19 |
| v2r-g-16 | bare | pass | pass | pass | 545 | 9.98 |
| v2r-g-16 | shipped | pass | fail | fail | 1953 | 33.96 |
| v2r-g-17 | bare | fail | pass | fail | 745 | 12.67 |
| v2r-g-17 | shipped | pass | pass | pass | 3010 | 48.85 |
| v2r-g-18 | bare | pass | pass | pass | 753 | 12.32 |
| v2r-g-18 | shipped | pass | pass | pass | 2802 | 48.36 |
| v2r-g-19 | bare | pass | pass | pass | 640 | 11.70 |
| v2r-g-19 | shipped | pass | fail | fail | 3072 | 50.12 |
| v2r-g-20 | bare | fail | fail | fail | 664 | 14.65 |
| v2r-g-20 | shipped | fail | fail | fail | 2750 | 54.64 |
| v2r-s-01 | bare | pass | pass | pass | 550 | 10.27 |
| v2r-s-01 | shipped | pass | pass | pass | 2356 | 38.35 |
| v2r-s-02 | bare | pass | fail | fail | 668 | 11.39 |
| v2r-s-02 | shipped | pass | pass | pass | 2480 | 38.98 |
| v2r-s-03 | bare | pass | fail | fail | 561 | 10.29 |
| v2r-s-03 | shipped | pass | fail | fail | 2387 | 38.06 |
| v2r-s-04 | bare | pass | fail | fail | 593 | 10.14 |
| v2r-s-04 | shipped | pass | fail | fail | 2836 | 47.17 |
| v2r-s-05 | bare | pass | fail | fail | 393 | 8.53 |
| v2r-s-05 | shipped | pass | fail | fail | 1683 | 28.21 |
| v2r-s-06 | bare | pass | fail | fail | 436 | 8.36 |
| v2r-s-06 | shipped | pass | fail | fail | 1788 | 30.23 |
| v2r-s-07 | bare | fail | pass | fail | 523 | 9.00 |
| v2r-s-07 | shipped | pass | pass | pass | 2582 | 41.98 |
| v2r-s-08 | bare | pass | fail | fail | 562 | 13.71 |
| v2r-s-08 | shipped | pass | pass | pass | 2491 | 40.86 |
| v2r-s-09 | bare | pass | fail | fail | 679 | 12.10 |
| v2r-s-09 | shipped | pass | fail | fail | 2397 | 50.98 |
| v2r-s-10 | bare | pass | fail | fail | 703 | 12.32 |
| v2r-s-10 | shipped | pass | fail | fail | 2780 | 44.83 |
| v2r-r-01 | bare | pass | fail | fail | 719 | 13.30 |
| v2r-r-01 | shipped | pass | fail | fail | 2634 | 44.53 |
| v2r-r-02 | bare | pass | fail | fail | 695 | 11.93 |
| v2r-r-02 | shipped | pass | pass | pass | 2809 | 48.04 |
| v2r-r-03 | bare | pass | pass | pass | 684 | 12.63 |
| v2r-r-03 | shipped | pass | pass | pass | 2613 | 47.29 |
| v2r-r-04 | bare | pass | pass | pass | 650 | 13.13 |
| v2r-r-04 | shipped | pass | pass | pass | 2288 | 40.68 |
| v2r-r-05 | bare | pass | fail | fail | 650 | 12.59 |
| v2r-r-05 | shipped | pass | fail | fail | 2152 | 36.53 |
| v2r-r-06 | bare | pass | fail | fail | 535 | 10.82 |
| v2r-r-06 | shipped | pass | fail | fail | 2204 | 38.98 |
| v2r-r-07 | bare | pass | pass | pass | 727 | 13.55 |
| v2r-r-07 | shipped | pass | fail | fail | 2819 | 48.57 |
| v2r-r-08 | bare | pass | fail | fail | 741 | 12.81 |
| v2r-r-08 | shipped | pass | fail | fail | 2685 | 44.98 |
| v2r-r-09 | bare | pass | fail | fail | 602 | 11.86 |
| v2r-r-09 | shipped | pass | fail | fail | 2375 | 41.38 |
| v2r-r-10 | bare | pass | fail | fail | 580 | 10.69 |
| v2r-r-10 | shipped | pass | pass | pass | 2492 | 42.60 |
