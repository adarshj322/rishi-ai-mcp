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

- `bare`: 13/40 = 0.325 interval [0.2008, 0.4798]
- `shipped`: 22/40 = 0.550 interval [0.3983, 0.6929]

## Delta (with minus without)

- delta = +0.225 interval [0.075, 0.375]

## Per-item results

| item | arm | deterministic | judge | pass | out tokens | latency s |
|---|---|---|---|---|---|---|
| v2-g-01 | bare | pass | fail | fail | 3581 | 26.62 |
| v2-g-01 | shipped | pass | fail | fail | 3658 | 61.50 |
| v2-g-02 | bare | pass | fail | fail | 756 | 16.47 |
| v2-g-02 | shipped | pass | pass | pass | 3464 | 57.56 |
| v2-g-03 | bare | pass | fail | fail | 1079 | 17.81 |
| v2-g-03 | shipped | pass | pass | pass | 3283 | 56.27 |
| v2-g-04 | bare | pass | fail | fail | 810 | 15.61 |
| v2-g-04 | shipped | pass | fail | fail | 3639 | 59.38 |
| v2-g-05 | bare | fail | fail | fail | 875 | 21.89 |
| v2-g-05 | shipped | fail | pass | fail | 3112 | 53.09 |
| v2-g-06 | bare | fail | pass | fail | 886 | 15.75 |
| v2-g-06 | shipped | fail | pass | fail | 2997 | 53.08 |
| v2-g-07 | bare | pass | fail | fail | 856 | 18.30 |
| v2-g-07 | shipped | pass | fail | fail | 2982 | 50.07 |
| v2-g-08 | bare | pass | fail | fail | 702 | 20.84 |
| v2-g-08 | shipped | pass | pass | pass | 2943 | 48.75 |
| v2-g-09 | bare | pass | pass | pass | 795 | 15.93 |
| v2-g-09 | shipped | pass | pass | pass | 3832 | 64.34 |
| v2-g-10 | bare | pass | pass | pass | 667 | 13.19 |
| v2-g-10 | shipped | pass | pass | pass | 3072 | 55.79 |
| v2-g-11 | bare | pass | pass | pass | 705 | 12.49 |
| v2-g-11 | shipped | pass | fail | fail | 2337 | 51.11 |
| v2-g-12 | bare | pass | pass | pass | 631 | 11.45 |
| v2-g-12 | shipped | pass | pass | pass | 2857 | 48.31 |
| v2-g-13 | bare | pass | pass | pass | 399 | 7.67 |
| v2-g-13 | shipped | pass | pass | pass | 1819 | 31.36 |
| v2-g-14 | bare | pass | pass | pass | 517 | 12.12 |
| v2-g-14 | shipped | pass | pass | pass | 1593 | 28.58 |
| v2-g-15 | bare | pass | pass | pass | 692 | 15.79 |
| v2-g-15 | shipped | pass | pass | pass | 2394 | 43.59 |
| v2-g-16 | bare | pass | pass | pass | 682 | 17.64 |
| v2-g-16 | shipped | pass | pass | pass | 2718 | 48.23 |
| v2-g-17 | bare | fail | pass | fail | 844 | 20.08 |
| v2-g-17 | shipped | pass | pass | pass | 2864 | 47.46 |
| v2-g-18 | bare | fail | pass | fail | 911 | 16.82 |
| v2-g-18 | shipped | pass | pass | pass | 3093 | 54.72 |
| v2-g-19 | bare | fail | fail | fail | 789 | 15.36 |
| v2-g-19 | shipped | fail | fail | fail | 2606 | 47.74 |
| v2-g-20 | bare | pass | fail | fail | 660 | 14.38 |
| v2-g-20 | shipped | pass | pass | pass | 2172 | 37.33 |
| v2-s-01 | bare | pass | fail | fail | 459 | 10.87 |
| v2-s-01 | shipped | pass | fail | fail | 2221 | 49.99 |
| v2-s-02 | bare | pass | fail | fail | 567 | 11.06 |
| v2-s-02 | shipped | pass | fail | fail | 2444 | 38.84 |
| v2-s-03 | bare | pass | pass | pass | 680 | 11.53 |
| v2-s-03 | shipped | pass | pass | pass | 2916 | 53.92 |
| v2-s-04 | bare | pass | fail | fail | 658 | 13.89 |
| v2-s-04 | shipped | pass | pass | pass | 2825 | 50.62 |
| v2-s-05 | bare | pass | fail | fail | 621 | 11.73 |
| v2-s-05 | shipped | pass | pass | pass | 3154 | 55.36 |
| v2-s-06 | bare | pass | pass | pass | 734 | 13.82 |
| v2-s-06 | shipped | pass | pass | pass | 2857 | 49.79 |
| v2-s-07 | bare | pass | pass | pass | 528 | 10.80 |
| v2-s-07 | shipped | pass | pass | pass | 2427 | 48.17 |
| v2-s-08 | bare | pass | pass | pass | 537 | 12.32 |
| v2-s-08 | shipped | pass | pass | pass | 2211 | 37.13 |
| v2-s-09 | bare | pass | fail | fail | 741 | 13.62 |
| v2-s-09 | shipped | pass | fail | fail | 2521 | 43.52 |
| v2-s-10 | bare | pass | fail | fail | 657 | 13.26 |
| v2-s-10 | shipped | pass | fail | fail | 2689 | 47.68 |
| v2-r-01 | bare | pass | fail | fail | 617 | 13.49 |
| v2-r-01 | shipped | pass | fail | fail | 2455 | 42.54 |
| v2-r-02 | bare | pass | fail | fail | 617 | 11.57 |
| v2-r-02 | shipped | pass | fail | fail | 2599 | 43.94 |
| v2-r-03 | bare | pass | pass | pass | 671 | 12.87 |
| v2-r-03 | shipped | pass | pass | pass | 2648 | 44.84 |
| v2-r-04 | bare | pass | fail | fail | 726 | 14.72 |
| v2-r-04 | shipped | pass | pass | pass | 2329 | 40.29 |
| v2-r-05 | bare | pass | fail | fail | 722 | 13.84 |
| v2-r-05 | shipped | pass | fail | fail | 2166 | 39.23 |
| v2-r-06 | bare | pass | fail | fail | 683 | 13.49 |
| v2-r-06 | shipped | pass | fail | fail | 2590 | 46.51 |
| v2-r-07 | bare | pass | fail | fail | 804 | 16.13 |
| v2-r-07 | shipped | pass | fail | fail | 3239 | 56.42 |
| v2-r-08 | bare | pass | fail | fail | 858 | 16.22 |
| v2-r-08 | shipped | pass | fail | fail | 3085 | 53.38 |
| v2-r-09 | bare | pass | fail | fail | 794 | 14.54 |
| v2-r-09 | shipped | pass | pass | pass | 2556 | 44.01 |
| v2-r-10 | bare | pass | fail | fail | 735 | 13.90 |
| v2-r-10 | shipped | pass | fail | fail | 2432 | 41.98 |
