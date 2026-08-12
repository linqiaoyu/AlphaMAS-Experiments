# Formal M0 Post-run Audit

**M0 POST-RUN AUDIT PASSED — FORMAL M0 PUBLICLY ARCHIVED AND RESEARCH-FROZEN**

This report is a read-only audit of frozen Formal M0 artefacts. No experiment runner, resume operation, force operation, LLM provider, or paid API was invoked by the audit.

## Experiment identity

- Public archive: [AlphaMAS-Experiments](https://github.com/linqiaoyu/AlphaMAS-Experiments)
- Experiment: `M0_original_prompt_2024H1`; successful run: `20260812T082530978211Z_2535896c`.
- Original interrupted lineage: `20260811T210814251902Z_2535896c`; the successful run is its legal resume.
- Source: `baseline-m0` at `2535896c8b1070b19c06fa6a936663babb4356f7`; Graph SHA256 `5b1b6e1c132c13f9830b377ba9d54bf0c792b087e9917af5f0ada9cc895d661e`; protocol SHA256 `bb08f3e169d32ff44a40988933fd8e58638596f5a1a04f3d0e1e22d8e4b116d7`.
- Snapshot SHA256: AAPL `5428fc2c672f3b68c7c3e83b4a22bd5b7330c95a8b4194695762539d9d8a5af3`, AMZN `c4b5c747d75ba658c6f6833348783e3f8a8c571380c930de20cf9fb7dd6b1444`, JPM `74cf77b77b0a83ce8e6246578d4da30bf7622558e8973bda71344b99b9dfd6fc`, SPY `22e6996ebf963787f40d54bfc59e1ca088fa698cb82b639768504dbdbb2d25ac`.
- Environment: Python 3.12.10, macOS-26.6.1-arm64-arm-64bit; uv.lock SHA256 `beec81b017ae7608e7ff8a529476ed637163af7004efb7c7111a8bd081ae5d29`.

## Validation

The official validation report passed. It records 26/26 decisions for each of AAPL, AMZN, and JPM (78/78 total), zero decision failures, complete daily equity, no future data visibility, no duplicate fills, valid snapshot checksums, complete agent cases, and a complete final Memory archive.

## Exact DeepSeek API cost

- Model: `deepseek-v4-flash`; unique billed provider requests: **2262**.
- Prompt cache-hit tokens: 5,221,632; uncached prompt tokens: 16,508,830; completion tokens: 2,912,553; total tokens: 24,643,015.
- Exact calculated cost: **$3.1413716096 USD = ¥22.6178755891** under the frozen ¥7.20/USD reporting conversion.
- Per-decision RMB cost: mean ¥0.28997276; median ¥0.29001980; min ¥0.24330394; max ¥0.33599821.
- Cache-hit prompt share: 24.0291%; uncached share: 75.9709%; estimated prompt-cache saving: $0.71640791 / ¥5.15813695.
- Pricing provenance: DeepSeek official Models & Pricing page retrieved 2026-08-12; cache-hit $0.0028/M, cache-miss $0.14/M, output $0.28/M. Reasoning tokens were absent from provider artefacts.
- Resume deduplication: the 39 original cases are represented by `cache_origin` usage records and the 39 resumed cases by `live_request` records. Cache-origin rows are preserved original billed requests, not extra resumed charges.

## Decision behaviour

| Scope | BUY | HOLD | SELL | No-op | Fills | Avg exposure | Time in market | Turnover | Transaction cost |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| AAPL | 1 | 20 | 5 | 25 | 1 | 21.6000% | 21.6000% | 0.98342139 | 99.92504997 |
| AMZN | 2 | 22 | 2 | 23 | 3 | 72.0000% | 72.0000% | 3.01671228 | 314.93888886 |
| JPM | 2 | 23 | 1 | 24 | 2 | 46.3671% | 46.4000% | 1.92586347 | 208.02639464 |
| equal_weight_aggregate | 5 | 65 | 8 | 72 | 6 | 46.6557% | 46.6667% | 1.98351665 | 622.89033347 |

M0 is visibly HOLD-heavy in this formal sample. Aggregate exposure is conservative in the descriptive sense that the strategy spent 46.67% of sessions in the market, but this audit does not label that superior risk management. Signal count differs from actual trade count because HOLD preserves the current target and repeated BUY/SELL signals can be no-ops when the account is already full or flat.

## Performance and benchmarks

| Series | Cumulative return | Annualized return | Volatility | Sharpe | Sortino | Max drawdown | Calmar |
|---|---:|---:|---:|---:|---:|---:|---:|
| AAPL | 18.0689% | 40.1517% | 14.4641% | 2.40517741 | 6.25896288 | 4.2369% | 9.47676607 |
| AMZN | 14.9272% | 32.6767% | 19.2761% | 1.56287955 | 2.52455225 | 8.1354% | 4.01659478 |
| JPM | 8.6942% | 18.4625% | 13.2601% | 1.34521388 | 1.71405745 | 8.1678% | 2.26041927 |
| equal_weight_m0 | 13.8968% | 30.2704% | 9.6526% | 2.78888121 | 4.75391091 | 5.0090% | 6.04315556 |
| AAPL_buy_and_hold | 24.4458% | 55.9640% | 24.4355% | 1.94014857 | 3.49559232 | 15.3397% | 3.64831377 |
| AMZN_buy_and_hold | 36.1593% | 87.2486% | 24.6723% | 2.66648596 | 4.85745149 | 8.1354% | 10.72454466 |
| JPM_buy_and_hold | 20.2669% | 45.5048% | 18.9662% | 2.07411428 | 2.83765727 | 9.5207% | 4.77955413 |
| equal_weight_buy_and_hold | 26.9573% | 62.4274% | 14.1183% | 3.50887506 | 6.11624469 | 6.1699% | 10.11805549 |
| SPY_buy_and_hold | 19.0010% | 42.4093% | 10.5370% | 3.40977462 | 5.61128858 | 5.3376% | 7.94535774 |

The formal equal-weight M0 aggregate cumulative return is 13.8968%; the newly constructed equal-weight Buy & Hold is 26.9573%. M0 minus equal-weight Buy & Hold cumulative return is -13.0605%; Sharpe difference is -0.71999385; Sortino difference is -1.36233378; maximum-drawdown difference is -0.01160853; Calmar difference is -4.07489992.

## Decision outcomes

Every one of the 78 weekly decisions has a row in `analysis/decision_outcomes.csv`, joined to the frozen decision timeline and weekly-performance artefacts. `analysis/decision_outcome_summary.csv` gives descriptive BUY/HOLD/SELL summaries for all stocks and each stock. No labels, directional-accuracy score, Macro-F1, or classification benchmark was created.

## Source availability

Historical `yfinance.get_news` was unavailable in 78/78 cases; global-news unavailability produced 314 records. Fundamentals were blocked in 78/78 cases. Social live-only sources were blocked in 78/78 cases. Macro live-only sources were blocked in 78/78 cases. Approximation-capability records existed for 78/78 cases; they were unavailable rather than treated as verified historical evidence.

All case-level source records are in `analysis/source_availability_by_case.csv`, with source, analyst mapping, stock, decision week, capability, and status. The source gaps are observations that may motivate future dataset work; FinMultiTime was not processed in this task.

## Memory behaviour

Each symbol has 26 immutable Memory entries: 25 resolved with reflections and one final pending entry at 2024-06-28. The first reflection becomes visible at 2024-01-12; all 25 reflections per symbol pass the five-trading-session maturity check, with zero premature or duplicate reflections. The final pending entry matches the formal experiment end design.

## Archive and limitations

The complete frozen source bundle is stored at `agent_outputs/formal_m0_complete_bundle.tar.gz` (19573036 bytes; SHA256 `0eb31fe83731da254e7d90e7104881b96d42028b3410ba5663b5a59ca8f83864`; 4051 source files); browsable inputs, analysis-ready files, tables, metrics, Memory, provenance, and validation are kept alongside it. `SHA256SUMS` is generated after all archive content is finalized.

Public repository verification status: `pending_publication_verification`. The recorded verification metadata is in `provenance/remote_verification.json` when publication has completed.

The RMB figure is conditional on the explicit ¥7.20/USD reporting assumption; the underlying usage calculation is exact in USD under the official DeepSeek prices. M0 is a 2024H1 baseline and does not establish long-term profitability or generalize to other regimes. Results are preserved regardless of benchmark-relative performance.

## Research integrity

New LLM calls: 0. New paid API calls: 0. M0 rerun: NO. Resume executed by audit: NO. Force executed: NO. M1/FinMultiTime/Qwen-VLM/Agentic RL/M2/M3: not started or not run.

**M0 POST-RUN AUDIT PASSED — FORMAL M0 PUBLICLY ARCHIVED AND RESEARCH-FROZEN**
