# M1 real-Agent pilot preflight — blocked

**PILOT ONLY**

**NOT FORMAL M1 RESULT**

**NOT USED FOR PERFORMANCE CLAIMS**

The canonical four-case real-Agent trajectory was not started. The deterministic
no-LLM preflight found that the weekly-backtest graph resolver does not propagate
the operational `finmultitime_input_root` from the fully resolved pilot config
into the `TradingAgentsGraph` config. Graph startup therefore fails closed with:

`FrozenEvidenceError: FinMultiTime evidence is enabled but finmultitime_input_root is missing`

This occurred before model-client construction and before any DeepSeek request.
Per the pilot stop policy, no source patch was made and none of the four cases
was attempted.

Verdict:

`M1 REAL-AGENT PILOT BLOCKED — CORRECTNESS REVIEW REQUIRED`

