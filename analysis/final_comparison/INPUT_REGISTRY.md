# Frozen Input Registry

All entries were resolved mechanically from official freeze/audit records. Pilot and development runs were excluded. Paths and full SHA256 values are in `input_registry.json`.

| System | Scientific role | Official run ID | Source SHA | Validation |
| --- | --- | --- | --- | --- |
| M0 | Historical-safe Prompt Trader baseline | 20260812T082530978211Z_2535896c | 2535896c8b1070b19c06fa6a936663babb4356f7 | PASS |
| M1 | PIT-safe FinMultiTime information treatment | 20260814T015553499023Z_ac0d1b00 | ac0d1b006d8019748702fda38399a4316befb9b0 | PASS |
| M2 | Full Agentic RL: global pretraining plus online adaptation | 20260817T101217082243Z_6306ea4e | 6306ea4ea20cda501c6238db80c34d27bbc16bea | PASS |
| A1 | Ablation: global pretraining only | 20260817T221009081674Z_11ae1ce4 | 11ae1ce4a3bac6245dbc39c073bcfc2ac0bba16b | PASS |
| A2 | Ablation: online adaptation only | 20260818T204749061036Z_ae0f36b1 | ae0f36b16a17a1321c17c630fb6a52e10dd23fcd | PASS |
| ARMA | Contextual classical ARMA(1,1) benchmark | ARMA11_2024H1 | d6c2b11cc4646dc06c435fe10a027d8f867e2791 | PASS |

Market snapshots: `AAPL=5428fc2c672f3b68c7c3e83b4a22bd5b7330c95a8b4194695762539d9d8a5af3`, `AMZN=c4b5c747d75ba658c6f6833348783e3f8a8c571380c930de20cf9fb7dd6b1444`, `JPM=74cf77b77b0a83ce8e6246578d4da30bf7622558e8973bda71344b99b9dfd6fc`, `SPY=22e6996ebf963787f40d54bfc59e1ca088fa698cb82b639768504dbdbb2d25ac`.
