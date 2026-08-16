# M2-10 Agentic RL Architecture Preregistration

This directory preregisters `M2-PA-CTPPO-v1` (**Prompt-Anchored Counterfactual
Tree PPO**) before the canonical TRAIN counterfactual tree is constructed. It is
an internal project method name, not a claim of algorithmic novelty or
state-of-the-art performance.

The method preserves the frozen `M2-SEMANTIC-STATE-v1` 3,080-dimensional Actor
observation and the frozen `R3_HOLD_RELATIVE_DRAWDOWN_UTILITY` proposal-level
reward. Eight independent symbol episodes each begin with $100,000 cash and no
position, then traverse seven weekly decisions as a complete, unpruned,
history-preserving BUY/HOLD/SELL tree. The resulting contract requires 8,744
decision nodes, 26,232 action edges, and 17,496 terminal leaves.

The shared 1,024-to-16 semantic projection is applied to the Research Manager,
Prompt Trader, and residual embeddings. Their projected representations plus
agreement, Prompt action, and portfolio state form a 56-dimensional bottleneck.
Separate 56-to-32 Actor and Critic trunks produce a bounded gated residual over
the full-support Prompt prior and a scalar state value. The architecture has
exactly 20,197 trainable parameters; only the 165 residual-head, gate-head, and
value-head parameters may adapt independently per symbol during Formal M2.

Pretraining uses exact old-policy tree occupancy, exact backward policy
evaluation, and the exact three-action expectation inside a clipped PPO
surrogate. It uses raw R3, gamma 1, no GAE, no action sampling, no advantage
standardisation, no entropy bonus, and no extra Prompt-KL loss. This task does
not train a canonical policy.

The only future global learning rates are `1e-4`, `3e-4`, and `1e-3`; the only
candidate checkpoints are iterations 25, 50, and 100. Future VALIDATION
selection is frozen to equal-weight mean sequential R3 across the 16 decisions,
with deterministic tie-breaks recorded in `architecture_plan.json`.

VALIDATION performance, FINAL_HOLDOUT, E2E_PILOT performance, Formal 2024 data,
market benchmarks, and paid model calls are outside M2-10. Online learning rate
and online update epochs remain explicitly deferred.
