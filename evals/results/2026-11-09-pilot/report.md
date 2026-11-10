# Equal-cost bar — pilot report

Pilot run: the noise floor only. No verdict is taken from this run (evals/README.md §4.2(d)).

- n = 26 items
- SE rule: rule 1: 0.5/sqrt(n)
- SE = 0.098058  (computed before any item was scored)
- Locked gate: delta > 0.098058
- Models: arms `deepseek-v4.1-flash`, judge `muse-spark-1.3-contributor`
- Budget per item per arm: 6000 output tokens
- Engine: 1.5.1 (/home/adarsh/cursorProjects/dashaflow/src/dashaflow/__init__.py)

Reported with intervals only. No trophy language, no external comparison, no point estimate standing alone (evals/README.md §4.3).

## Arms

- `bare`: 4/26 = 0.154 interval [0.0615, 0.3353]
- `without`: 5/26 = 0.192 interval [0.0851, 0.3788]
- `with`: 4/26 = 0.154 interval [0.0615, 0.3353]

## Delta (with minus without)

- delta = -0.038 interval [-0.3173, 0.2502]

## Per-item results

| item | arm | deterministic | judge | pass | out tokens | latency s |
|---|---|---|---|---|---|---|
| g-01 | bare | fail | fail | fail | 748 | 8.31 |
| g-01 | without | pass | fail | fail | 3235 | 27.04 |
| g-01 | with | fail | fail | fail | 2900 | 22.35 |
| g-02 | bare | pass | fail | fail | 709 | 9.05 |
| g-02 | without | fail | fail | fail | 2908 | 25.76 |
| g-02 | with | fail | fail | fail | 2930 | 22.20 |
| g-03 | bare | fail | fail | fail | 609 | 6.68 |
| g-03 | without | fail | fail | fail | 3017 | 25.51 |
| g-03 | with | fail | fail | fail | 3681 | 28.65 |
| g-04 | bare | fail | fail | fail | 627 | 6.94 |
| g-04 | without | pass | fail | fail | 3232 | 27.58 |
| g-04 | with | pass | fail | fail | 3304 | 25.52 |
| g-05 | bare | fail | fail | fail | 770 | 9.17 |
| g-05 | without | pass | fail | fail | 3216 | 28.59 |
| g-05 | with | pass | fail | fail | 2820 | 21.70 |
| g-06 | bare | fail | fail | fail | 602 | 6.26 |
| g-06 | without | pass | pass | pass | 3085 | 26.37 |
| g-06 | with | pass | fail | fail | 3922 | 27.31 |
| g-07 | bare | fail | fail | fail | 588 | 7.07 |
| g-07 | without | fail | fail | fail | 2926 | 27.14 |
| g-07 | with | pass | fail | fail | 3241 | 24.33 |
| g-08 | bare | fail | fail | fail | 661 | 7.53 |
| g-08 | without | fail | fail | fail | 3285 | 30.12 |
| g-08 | with | fail | fail | fail | 3549 | 25.46 |
| g-09 | bare | fail | fail | fail | 706 | 7.17 |
| g-09 | without | fail | fail | fail | 2497 | 23.57 |
| g-09 | with | pass | pass | pass | 2664 | 21.99 |
| g-10 | bare | fail | fail | fail | 522 | 7.47 |
| g-10 | without | fail | fail | fail | 2947 | 28.16 |
| g-10 | with | fail | fail | fail | 3846 | 30.14 |
| g-11 | bare | pass | fail | fail | 652 | 7.05 |
| g-11 | without | pass | fail | fail | 3078 | 27.36 |
| g-11 | with | pass | fail | fail | 3717 | 26.65 |
| g-12 | bare | pass | fail | fail | 686 | 8.71 |
| g-12 | without | pass | fail | fail | 3096 | 29.34 |
| g-12 | with | fail | fail | fail | 4445 | 33.31 |
| s-01 | bare | pass | pass | pass | 280 | 4.52 |
| s-01 | without | pass | pass | pass | 2426 | 22.81 |
| s-01 | with | fail | pass | fail | 3075 | 23.77 |
| s-02 | bare | pass | fail | fail | 600 | 6.61 |
| s-02 | without | pass | fail | fail | 3142 | 26.01 |
| s-02 | with | pass | fail | fail | 3354 | 68.23 |
| s-03 | bare | pass | pass | pass | 502 | 43.58 |
| s-03 | without | pass | pass | pass | 2552 | 48.06 |
| s-03 | with | pass | pass | pass | 4132 | 79.26 |
| s-04 | bare | pass | fail | fail | 633 | 6.94 |
| s-04 | without | pass | fail | fail | 2734 | 25.19 |
| s-04 | with | pass | fail | fail | 3842 | 25.48 |
| s-05 | bare | pass | fail | fail | 579 | 6.43 |
| s-05 | without | pass | fail | fail | 3149 | 268.90 |
| s-05 | with | pass | fail | fail | 3732 | 26.23 |
| s-06 | bare | pass | fail | fail | 622 | 7.70 |
| s-06 | without | pass | fail | fail | 2636 | 24.32 |
| s-06 | with | pass | fail | fail | 3377 | 26.66 |
| s-07 | bare | pass | fail | fail | 25 | 1.74 |
| s-07 | without | pass | fail | fail | 1664 | 17.33 |
| s-07 | with | pass | fail | fail | 2061 | 16.77 |
| s-08 | bare | fail | fail | fail | 528 | 6.99 |
| s-08 | without | pass | fail | fail | 2176 | 21.61 |
| s-08 | with | fail | fail | fail | 2432 | 19.29 |
| r-01 | bare | pass | fail | fail | 686 | 8.91 |
| r-01 | without | pass | fail | fail | 2482 | 25.20 |
| r-01 | with | pass | fail | fail | 2522 | 21.50 |
| r-02 | bare | pass | fail | fail | 652 | 8.73 |
| r-02 | without | pass | fail | fail | 2580 | 25.20 |
| r-02 | with | pass | fail | fail | 3162 | 24.05 |
| r-03 | bare | pass | pass | pass | 544 | 6.93 |
| r-03 | without | pass | pass | pass | 2365 | 22.77 |
| r-03 | with | pass | pass | pass | 3010 | 24.78 |
| r-04 | bare | pass | fail | fail | 534 | 7.20 |
| r-04 | without | pass | fail | fail | 2935 | 27.91 |
| r-04 | with | pass | fail | fail | 3636 | 29.26 |
| r-05 | bare | pass | pass | pass | 514 | 5.95 |
| r-05 | without | pass | pass | pass | 2836 | 26.69 |
| r-05 | with | pass | pass | pass | 3398 | 26.22 |
| r-06 | bare | pass | fail | fail | 554 | 7.31 |
| r-06 | without | pass | fail | fail | 2314 | 23.12 |
| r-06 | with | pass | fail | fail | 3418 | 26.98 |
