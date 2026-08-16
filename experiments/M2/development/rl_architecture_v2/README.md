# M2-10A Corrected Agentic RL Architecture

This archive preregisters and freezes `M2-PA-CTPPO-v2`, **Prompt-Anchored
Counterfactual Tree PPO — Delayed-Credit Formulation**. It transparently
supersedes the blocked v1 method before any policy training or protected
evaluation.

The complete BUY/HOLD/SELL tree enumerates reachable portfolio states at the
seven frozen weekly decision closes and propagates exact old-policy occupancy.
Separately, every node/action receives an independently matured five-session
`R3_HOLD_RELATIVE_DRAWDOWN_UTILITY` local Trader-credit probe. Reward maturity
may occur before, on, or after the next weekly decision and never defines the
child portfolio state.

The corrected objective uses local `V_cf = sum_a pi_old(a|s) R3(s,a)` and
`A_cf = R3 - V_cf`. It contains no Bellman bootstrap, reward-to-go, gamma, GAE,
or action sampling. The Prompt prior, 20,197-parameter Actor/Critic,
165-parameter per-symbol fast boundary, PPO clip, future training candidates,
and protected evaluation boundaries remain unchanged.
