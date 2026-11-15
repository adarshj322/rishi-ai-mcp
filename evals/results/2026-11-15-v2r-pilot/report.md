# Equal-cost bar — pilot report

Pilot run: the noise floor only. No verdict is taken from this run (evals/README.md §4.2(d)).

- n = 40 items
- SE rule: rule 1: 0.5/sqrt(n)
- SE = 0.079057  (computed before any item was scored)
- Locked gate: delta > 0.079057
- Models: arms `glm-5.3-flash`, judge `deepseek-v4.1-flash`
- Budget per item per arm: 12000 output tokens
- Engine: 1.5.1 (/home/adarsh/cursorProjects/dashaflow/src/dashaflow/__init__.py)

Reported with intervals only. No trophy language, no external comparison, no point estimate standing alone (evals/README.md §4.3).

## Arms

- `bare`: 15/40 = 0.375 interval [0.2422, 0.5297]
- `shipped`: 23/40 = 0.575 interval [0.4219, 0.7149]

## Delta (with minus without)

- delta = +0.200 interval [0.025, 0.35]

## Per-item results

| item | arm | deterministic | judge | pass | out tokens | latency s |
|---|---|---|---|---|---|---|
| v2r-g-01 | bare | pass | fail | fail | 636 | 11.29 |
| v2r-g-01 | shipped | pass | fail | fail | 3110 | 52.14 |
| v2r-g-02 | bare | fail | pass | fail | 606 | 10.05 |
| v2r-g-02 | shipped | pass | pass | pass | 3133 | 60.06 |
| v2r-g-03 | bare | pass | pass | pass | 862 | 14.66 |
| v2r-g-03 | shipped | pass | pass | pass | 3239 | 50.56 |
| v2r-g-04 | bare | pass | pass | pass | 629 | 11.30 |
| v2r-g-04 | shipped | pass | pass | pass | 3751 | 55.66 |
| v2r-g-05 | bare | pass | fail | fail | 847 | 15.57 |
| v2r-g-05 | shipped | pass | fail | fail | 3113 | 48.48 |
| v2r-g-06 | bare | pass | fail | fail | 863 | 15.32 |
| v2r-g-06 | shipped | pass | fail | fail | 3470 | 52.41 |
| v2r-g-07 | bare | pass | pass | pass | 863 | 14.32 |
| v2r-g-07 | shipped | pass | pass | pass | 3073 | 48.85 |
| v2r-g-08 | bare | pass | pass | pass | 768 | 14.33 |
| v2r-g-08 | shipped | pass | pass | pass | 3311 | 49.90 |
| v2r-g-09 | bare | pass | pass | pass | 599 | 11.23 |
| v2r-g-09 | shipped | pass | pass | pass | 2518 | 47.11 |
| v2r-g-10 | bare | pass | fail | fail | 827 | 22.61 |
| v2r-g-10 | shipped | pass | fail | fail | 3140 | 49.26 |
| v2r-g-11 | bare | pass | fail | fail | 796 | 13.88 |
| v2r-g-11 | shipped | pass | pass | pass | 3055 | 49.21 |
| v2r-g-12 | bare | fail | fail | fail | 740 | 12.74 |
| v2r-g-12 | shipped | pass | pass | pass | 3364 | 52.88 |
| v2r-g-13 | bare | fail | pass | fail | 562 | 11.32 |
| v2r-g-13 | shipped | pass | pass | pass | 2141 | 34.20 |
| v2r-g-14 | bare | pass | fail | fail | 731 | 14.85 |
| v2r-g-14 | shipped | pass | pass | pass | 2105 | 35.63 |
| v2r-g-15 | bare | pass | pass | pass | 482 | 7.96 |
| v2r-g-15 | shipped | pass | pass | pass | 1679 | 35.22 |
| v2r-g-16 | bare | pass | pass | pass | 464 | 8.69 |
| v2r-g-16 | shipped | pass | fail | fail | 1463 | 24.32 |
| v2r-g-17 | bare | pass | pass | pass | 739 | 13.30 |
| v2r-g-17 | shipped | pass | pass | pass | 2933 | 48.21 |
| v2r-g-18 | bare | pass | pass | pass | 721 | 12.93 |
| v2r-g-18 | shipped | pass | pass | pass | 2346 | 38.69 |
| v2r-g-19 | bare | pass | fail | fail | 672 | 12.20 |
| v2r-g-19 | shipped | pass | fail | fail | 2861 | 46.30 |
| v2r-g-20 | bare | fail | fail | fail | 729 | 13.68 |
| v2r-g-20 | shipped | fail | fail | fail | 2687 | 50.20 |
| v2r-s-01 | bare | pass | fail | fail | 607 | 10.38 |
| v2r-s-01 | shipped | pass | pass | pass | 2498 | 39.88 |
| v2r-s-02 | bare | pass | fail | fail | 534 | 9.46 |
| v2r-s-02 | shipped | pass | pass | pass | 2267 | 36.61 |
| v2r-s-03 | bare | pass | fail | fail | 495 | 8.11 |
| v2r-s-03 | shipped | pass | fail | fail | 2167 | 34.54 |
| v2r-s-04 | bare | pass | fail | fail | 680 | 11.17 |
| v2r-s-04 | shipped | pass | fail | fail | 3008 | 47.49 |
| v2r-s-05 | bare | pass | fail | fail | 380 | 8.11 |
| v2r-s-05 | shipped | pass | fail | fail | 1738 | 29.08 |
| v2r-s-06 | bare | pass | fail | fail | 462 | 8.58 |
| v2r-s-06 | shipped | pass | fail | fail | 1864 | 29.48 |
| v2r-s-07 | bare | pass | pass | pass | 572 | 10.02 |
| v2r-s-07 | shipped | pass | pass | pass | 2596 | 39.81 |
| v2r-s-08 | bare | pass | pass | pass | 576 | 11.66 |
| v2r-s-08 | shipped | pass | pass | pass | 2307 | 35.25 |
| v2r-s-09 | bare | pass | fail | fail | 790 | 13.21 |
| v2r-s-09 | shipped | pass | fail | fail | 2773 | 52.02 |
| v2r-s-10 | bare | pass | fail | fail | 718 | 11.92 |
| v2r-s-10 | shipped | pass | fail | fail | 2946 | 52.91 |
| v2r-r-01 | bare | pass | fail | fail | 599 | 10.89 |
| v2r-r-01 | shipped | pass | fail | fail | 2790 | 43.95 |
| v2r-r-02 | bare | pass | pass | pass | 621 | 10.21 |
| v2r-r-02 | shipped | pass | fail | fail | 2848 | 46.82 |
| v2r-r-03 | bare | pass | pass | pass | 606 | 11.83 |
| v2r-r-03 | shipped | pass | pass | pass | 2212 | 40.71 |
| v2r-r-04 | bare | pass | pass | pass | 661 | 14.37 |
| v2r-r-04 | shipped | pass | pass | pass | 2455 | 37.32 |
| v2r-r-05 | bare | pass | fail | fail | 600 | 10.54 |
| v2r-r-05 | shipped | pass | pass | pass | 2404 | 38.73 |
| v2r-r-06 | bare | pass | pass | pass | 661 | 12.56 |
| v2r-r-06 | shipped | pass | pass | pass | 2368 | 38.68 |
| v2r-r-07 | bare | pass | fail | fail | 982 | 16.13 |
| v2r-r-07 | shipped | pass | pass | pass | 2761 | 44.00 |
| v2r-r-08 | bare | pass | fail | fail | 814 | 14.37 |
| v2r-r-08 | shipped | pass | fail | fail | 2704 | 45.73 |
| v2r-r-09 | bare | pass | fail | fail | 480 | 8.46 |
| v2r-r-09 | shipped | pass | fail | fail | 2631 | 43.19 |
| v2r-r-10 | bare | pass | fail | fail | 665 | 12.15 |
| v2r-r-10 | shipped | pass | pass | pass | 2308 | 38.92 |
