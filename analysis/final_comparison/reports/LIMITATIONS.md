# Limitations

- The evaluation contains three stocks only and treats AAPL, AMZN and JPM as heterogeneous cases.
- It covers one 2024H1 market regime, in which all Buy & Hold references had strong positive returns.
- The paradigm is descriptive controlled evaluation plus cross-asset consistency, not inferential statistical significance.
- LLM outputs can remain nondeterministic despite temperature 0.
- The policy froze the first complete correctness-valid trajectory rather than selecting a favourable rerun.
- RL development contexts were limited, with one frozen global choice and one frozen online hyperparameter choice.
- A1/A2 do not create a complete strict factorial test because M1 is not an equivalent RL “neither” architecture.
- Asset heterogeneity limits simple aggregation and makes the per-stock cases primary evidence.
- ARMA maintained high market exposure, so high return must not be equated automatically with timing alpha.
- No M3 or post-hoc optimisation was performed. A redesigned successor belongs to future work on a new untouched holdout, rather than reuse of the observed 2024H1 window.

These boundaries limit scope without invalidating the controlled within-protocol comparisons.
