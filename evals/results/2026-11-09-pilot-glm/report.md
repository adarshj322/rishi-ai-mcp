# Equal-cost bar — pilot report

Pilot run: the noise floor only. No verdict is taken from this run (evals/README.md §4.2(d)).

- n = 26 items
- SE rule: rule 1: 0.5/sqrt(n)
- SE = 0.098058  (computed before any item was scored)
- Locked gate: delta > 0.098058
- Models: arms `glm-5.3-flash`, judge `deepseek-v4.1-flash`
- Budget per item per arm: 12000 output tokens
- Engine: 1.5.1 (/home/adarsh/cursorProjects/dashaflow/src/dashaflow/__init__.py)

Reported with intervals only. No trophy language, no external comparison, no point estimate standing alone (evals/README.md §4.3).

## Arms

- `bare`: 1/26 = 0.038 interval [0.0068, 0.1889]
- `without`: 1/26 = 0.038 interval [0.0068, 0.1889]
- `with`: 4/26 = 0.154 interval [0.0615, 0.3353]

## Delta (with minus without)

- delta = +0.115 interval [-0.0385, 0.2692]

## Per-item results

| item | arm | deterministic | judge | pass | out tokens | latency s |
|---|---|---|---|---|---|---|
| g-01 | bare | pass | fail | fail | 4011 | 31.17 |
| g-01 | without | pass | fail | fail | 11342 | 83.11 |
| g-01 | with | fail | fail | fail | 7034 | 53.89 |
| g-02 | bare | fail | fail | fail | 3225 | 26.88 |
| g-02 | without | fail | fail | fail | 11930 | 91.53 |
| g-02 | with | fail | fail | fail | 6472 | 57.77 |
| g-03 | bare | pass | fail | fail | 2820 | 25.88 |
| g-03 | without | pass | fail | fail | 8946 | 72.05 |
| g-03 | with | pass | fail | fail | 9415 | 74.86 |
| g-04 | bare | pass | fail | fail | 2438 | 22.44 |
| g-04 | without | pass | fail | fail | 12000 | 90.77 |
| g-04 | with | pass | fail | fail | 11671 | 84.96 |
| g-05 | bare | fail | fail | fail | 776 | 9.62 |
| g-05 | without | pass | fail | fail | 2567 | 26.81 |
| g-05 | with | fail | fail | fail | 4606 | 45.23 |
| g-06 | bare | pass | fail | fail | 778 | 8.69 |
| g-06 | without | pass | pass | pass | 2647 | 27.35 |
| g-06 | with | pass | fail | fail | 4033 | 37.48 |
| g-07 | bare | pass | fail | fail | 743 | 8.38 |
| g-07 | without | pass | fail | fail | 2753 | 28.73 |
| g-07 | with | fail | fail | fail | 3326 | 35.57 |
| g-08 | bare | pass | fail | fail | 650 | 7.89 |
| g-08 | without | pass | fail | fail | 2569 | 28.75 |
| g-08 | with | pass | fail | fail | 4302 | 42.79 |
| g-09 | bare | fail | fail | fail | 781 | 8.92 |
| g-09 | without | fail | fail | fail | 2368 | 26.40 |
| g-09 | with | fail | fail | fail | 3543 | 36.76 |
| g-10 | bare | fail | fail | fail | 797 | 10.39 |
| g-10 | without | fail | fail | fail | 3441 | 39.47 |
| g-10 | with | fail | fail | fail | 3866 | 39.17 |
| g-11 | bare | pass | fail | fail | 689 | 8.41 |
| g-11 | without | pass | fail | fail | 2880 | 30.79 |
| g-11 | with | pass | pass | pass | 3777 | 39.74 |
| g-12 | bare | pass | fail | fail | 839 | 10.03 |
| g-12 | without | pass | fail | fail | 3465 | 39.78 |
| g-12 | with | pass | fail | fail | 2893 | 31.89 |
| s-01 | bare | fail | fail | fail | 300 | 4.50 |
| s-01 | without | pass | fail | fail | 1520 | 18.61 |
| s-01 | with | pass | fail | fail | 1984 | 24.69 |
| s-02 | bare | pass | fail | fail | 621 | 7.66 |
| s-02 | without | pass | fail | fail | 2946 | 33.55 |
| s-02 | with | pass | fail | fail | 3520 | 37.12 |
| s-03 | bare | pass | pass | pass | 518 | 7.12 |
| s-03 | without | pass | fail | fail | 2299 | 27.29 |
| s-03 | with | pass | pass | pass | 2796 | 31.72 |
| s-04 | bare | pass | fail | fail | 709 | 8.82 |
| s-04 | without | pass | fail | fail | 2400 | 27.19 |
| s-04 | with | pass | fail | fail | 3256 | 35.80 |
| s-05 | bare | pass | fail | fail | 637 | 8.23 |
| s-05 | without | pass | fail | fail | 2646 | 29.62 |
| s-05 | with | pass | fail | fail | 3809 | 40.60 |
| s-06 | bare | pass | fail | fail | 606 | 8.37 |
| s-06 | without | pass | fail | fail | 2819 | 33.35 |
| s-06 | with | pass | fail | fail | 2923 | 33.09 |
| s-07 | bare | pass | fail | fail | 56 | 2.31 |
| s-07 | without | pass | fail | fail | 988 | 14.54 |
| s-07 | with | pass | fail | fail | 1952 | 26.79 |
| s-08 | bare | pass | fail | fail | 470 | 6.64 |
| s-08 | without | pass | fail | fail | 1686 | 22.14 |
| s-08 | with | fail | fail | fail | 2655 | 32.51 |
| r-01 | bare | pass | fail | fail | 671 | 9.13 |
| r-01 | without | pass | fail | fail | 2205 | 27.74 |
| r-01 | with | pass | fail | fail | 2755 | 33.37 |
| r-02 | bare | pass | fail | fail | 722 | 9.89 |
| r-02 | without | pass | fail | fail | 2219 | 29.75 |
| r-02 | with | pass | fail | fail | 3247 | 38.31 |
| r-03 | bare | pass | fail | fail | 702 | 10.36 |
| r-03 | without | pass | fail | fail | 2616 | 33.82 |
| r-03 | with | pass | pass | pass | 3224 | 39.03 |
| r-04 | bare | pass | fail | fail | 803 | 11.59 |
| r-04 | without | pass | fail | fail | 2583 | 36.86 |
| r-04 | with | pass | fail | fail | 3268 | 39.90 |
| r-05 | bare | pass | fail | fail | 666 | 9.43 |
| r-05 | without | pass | fail | fail | 2742 | 35.49 |
| r-05 | with | pass | pass | pass | 3837 | 44.60 |
| r-06 | bare | pass | fail | fail | 569 | 9.22 |
| r-06 | without | pass | fail | fail | 2410 | 32.89 |
| r-06 | with | pass | fail | fail | 3798 | 46.73 |
