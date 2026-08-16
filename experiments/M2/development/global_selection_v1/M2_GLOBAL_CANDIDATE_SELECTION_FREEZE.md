# M2-12 Global Candidate Selection Freeze

The first complete correctness-valid run selected **C09** from exactly the nine
frozen M2-11 candidates. C09's canonical parameter SHA is
`6baafc03b0b63512b3a66a1ae8f1ce1ce7e774395787626b49905e7b72cd1841`.

Its mean sequential local R3 across the 16 frozen VALIDATION decisions is
`0.0011119952063548388`; worst-symbol cumulative R3 is
`-0.05822419930530598`; Prompt override rate is `0.125`. The primary metric had
no tie, so none of the ordered tie-breaks was invoked. Human override was not
permitted and did not occur.

The selected `model.pt` is byte-identical to the canonical M2-11 C09 file and
retains identical canonical parameter, Actor, and Critic identities. The audit-
only replay produced zero action, selected-reward, or primary-score mismatches.

M2-12 used VALIDATION only for the preregistered global checkpoint selection. No
candidate parameters were updated using VALIDATION. FINAL_HOLDOUT, E2E_PILOT,
Formal 2024H1, M1 performance, raw FinMultiTime, live market data, model APIs,
and AWS were not accessed or used.
