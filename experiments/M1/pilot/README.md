# M1 isolated out-of-window pilot archive

This directory is PILOT ONLY. It is not `experiments/M1/inputs/`, is not a
formal M1 input, is not part of the 78-case test set, and must not be used for
performance analysis.

The archived bundle contains exactly four AAPL cases:

- 2023-10-06
- 2023-10-13
- 2023-10-20
- 2023-10-27

The runtime must select it with `finmultitime_bundle_scope=PILOT` and the
explicit packet-manifest and bundle identities in the AlphaMAS pilot config.
FORMAL and PILOT scope are fail-closed and cannot cross-load one another.

The bundle is self-contained. The raw FinMultiTime mount is required only by
the isolated builder during input generation and is not a runtime dependency.
No Agent, LLM, Qwen, DeepSeek, paid API, AWS, Trader, execution, metrics, or
Memory-algorithm run is performed by this archive.
