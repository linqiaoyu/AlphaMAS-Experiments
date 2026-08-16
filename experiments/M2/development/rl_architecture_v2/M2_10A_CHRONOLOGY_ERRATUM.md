# M2-10A Chronology Erratum

## Original defect

The original plan commit was
`89c84945e19a5a532b7afc042300e2ea17377a79`; its blocked method runner was
`f779069ab4b133b5421ff4d9b6a972e44f48712e`. It incorrectly tied the next
weekly state to five-session R3 maturity.

The counterexample is exact:

```text
decision:        2023-05-26 close
action executes: 2023-05-30 open
child decision:  2023-06-02 close
reward maturity: 2023-06-05 close
```

May 29 was not an XNYS session. Consequently, the fifth subsequent session
after May 26 is June 5. Using the June 5 portfolio as the June 2 Actor state
would leak future information. The affected population is 216 depth-3 nodes
and 648 action edges.

## Corrected interpretation

State-transition time is distinct from reward-maturity time. The selected
action advances the actual sequential portfolio only through the next frozen
weekly decision close. Independently, the frozen reward simulator evaluates
BUY, HOLD, and SELL from the parent state over its five-session credit horizon.
The local credit cannot depend on descendant actions and cannot overwrite the
weekly child state.

The tree is therefore used to enumerate reachable weekly states and calculate
old-policy occupancy. Overlapping R3 probes are not chained into Bellman
returns. The corrected scalar target is local counterfactual value `V_cf`, and
the policy advantage is local `R3 - V_cf`.

## Research validity

The change is a correctness correction required to preserve point-in-time
validity. It was made before policy training, validation-performance inspection
or Holdout use, and does not alter the frozen data split, reward definition,
representation, Prompt prior or trading protocol.

Training performed before detection: **NO**. VALIDATION performance inspected:
**NO**. Holdout inspected: **NO**.
