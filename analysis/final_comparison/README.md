# COMPARE-01 Final Comparison

This directory contains the reproducible final controlled comparison of frozen M0/M1/M2/A1/A2/ARMA results and market references.

Regenerate offline from the repository root:

```bash
/Users/yulinqiao/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 analysis/final_comparison/scripts/build_compare01.py
```

The script uses only Python's standard library and frozen repository artifacts. It performs integrity and comparability gates before writing analytical results. It does not call DeepSeek, Qwen, AWS, a GPU, market-data services, or any experiment runner. Official metrics remain authoritative; terminal cumulative return is recalculated only as a validation check.

Start with `tables/THESIS_MAIN_RESULTS_TABLE.md`, `tables/THESIS_CONTROLLED_COMPARISONS.md`, `reports/RESEARCH_QUESTION_ANSWERS.md`, and `COMPARE_01_AUDIT.md`.

## Unit convention

- Percentage levels are displayed with `%`.
- Absolute differences between percentage-valued levels are displayed in percentage points (`pp`).
- Ratios such as Sharpe, Calmar, Sortino and turnover are unitless.
- Machine-readable derived data retain decimal-fraction storage unless explicit metadata states otherwise; see `data/metric_units.json`.
- Monetary values use `$`; counts are integers.
