# RQ3 — RL Mechanisms

Canonical treatments: `M2 = global pretraining + online adaptation`; `A1 = global pretraining only`; `A2 = online adaptation only`.

## Aggregate comparison

A1 exceeded M2 return by 13.91% and A2 exceeded M2 by 10.14%. A1 also had much higher exposure (59.90%) than M2 (27.73%), whereas A2 exposure was 33.07%. A1 and A2 each incurred fewer trades and lower costs than M2. A1 exceeded A2 return by 3.77%, but A2 had the lower MDD.

## Asset mechanisms

- AAPL: all three RL treatments stayed in cash, despite different action pathways and extensive M2/A2 parameter updating.
- AMZN: M2 returned 6.69% at 60.80% exposure; A1 returned 27.35% at 92.00%; A2 returned 36.16% at 99.20%. Earlier and more persistent participation coincided with the higher ablation returns.
- JPM: A1 entered and returned 20.11%; M2 traded twice and returned -0.96%; A2 remained in cash and returned 0%. The mechanisms therefore changed whether and when the systems participated.

## Interpretation guardrail

The combined Full-M2 configuration performed materially worse than either single-mechanism ablation in aggregate. The pattern is consistent with a negative or non-additive relationship between global pretraining and delayed online adaptation. It is not a formal factorial interaction proof: M1 uses the Prompt Trader without the A1/A2/M2 RL policy layer and is not an equivalent RL “neither” cell. No p-values or significance claims are made.
