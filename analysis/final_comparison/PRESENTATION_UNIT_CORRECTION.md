# COMPARE-01 Presentation Unit Correction

- Previous COMPARE-01 commit: `198dcb01b098ba22ae1600117ab39df8a1c9f96f`
- Correction type: `PRESENTATION_UNIT_SEMANTICS`
- Affected concept: percentage levels versus absolute percentage-point differences
- Scientific metrics changed: NO
- Experiment artifacts changed: NO
- Analytical deltas changed: NO
- Conclusions changed: NO
- Figures/tables/reports regenerated: YES

Percentage levels use `%`; absolute differences between percentage-valued levels use `pp` in tables and “percentage points” in prose. Ratios remain unitless. Machine-readable analytical values remain decimal fractions, with explicit display semantics in `data/metric_units.json`.

## Files reviewed

- `README.md`
- `tables/THESIS_MAIN_RESULTS_TABLE.md`
- `tables/THESIS_MAIN_RESULTS_TABLE.tex`
- `tables/THESIS_CONTROLLED_COMPARISONS.md`
- `tables/THESIS_CONTROLLED_COMPARISONS.tex`
- `tables/aggregate_primary.csv`
- `tables/aggregate_primary.md`
- `tables/aggregate_primary.tex`
- `tables/aggregate_secondary.csv`
- `tables/aggregate_secondary.md`
- `tables/aggregate_secondary.tex`
- `tables/AAPL_primary.csv`
- `tables/AAPL_primary.md`
- `tables/AAPL_primary.tex`
- `tables/AMZN_primary.csv`
- `tables/AMZN_primary.md`
- `tables/AMZN_primary.tex`
- `tables/JPM_primary.csv`
- `tables/JPM_primary.md`
- `tables/JPM_primary.tex`
- `tables/controlled_deltas.csv`
- `tables/cross_asset_consistency.csv`
- `tables/exposure_participation.csv`
- `reports/RQ1_INFORMATION_CONTRIBUTION.md`
- `reports/RQ2_AGENTIC_RL_CONTRIBUTION.md`
- `reports/RQ3_RL_MECHANISMS.md`
- `reports/RESEARCH_QUESTION_ANSWERS.md`
- `reports/THESIS_FINDINGS_SUMMARY.md`
- `reports/AAPL_CASE_ANALYSIS.md`
- `reports/AMZN_CASE_ANALYSIS.md`
- `reports/JPM_CASE_ANALYSIS.md`
- `reports/MARKET_PARTICIPATION.md`
- `reports/ARMA_CONTEXT.md`
- `reports/PARAMETER_TO_ECONOMIC_BEHAVIOUR.md`
- `reports/CLAIM_GUARDRAILS.md`
- `reports/LIMITATIONS.md`
- `figures/figure_01_aggregate_cumulative_return.svg`
- `figures/figure_02_aggregate_equity_curves.svg`
- `figures/figure_03_per_stock_returns.svg`
- `figures/figure_04_return_vs_exposure.svg`
- `figures/figure_05_risk_return.svg`
- `figures/figure_06_controlled_return_deltas.svg`
- `figures/figure_07_trading_intensity_cost.svg`
- `figures/figure_08_rl_action_pathway.svg`
