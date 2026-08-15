# M2-06 Final Evidence Corpus Lineage Audit

**PRE-FORMAL DEVELOPMENT — M2-06 LINEAGE AUDIT — DOES NOT MODIFY FROZEN CORPUS**

This separate audit archive records the clean reproduction of the frozen M2-06
evidence corpus. It is not part of, and does not alter, the frozen corpus at
`../preformal_evidence_v1/`.

Clean source commit `3cef79b9536e4714cc5f532eada84f66fd6e8142` rebuilt the
corpus from pre-Qwen inputs commit
`a9d3c554a9eb0ecf401a2064d12d5fb901e55165` and the frozen Qwen caption
bundle in corpus commit `6b2406f1e12e1988c27b44880a1e153a9b750c2e`.

The rebuilt corpus identity is
`3e9bb6e66fcd998c0b4deff30f7d5728c563126d3a1b976e21bbf034174e4420`.
All 96 structured packets, all 96 rendered packets, all 355 research files,
the 353-entry final manifest, and the generated README are byte-identical to
the frozen reference. Built-in double-generation determinism passed.

No raw FinMultiTime access, Qwen inference, DeepSeek call, Agent execution, or
AWS action occurred. FINAL_HOLDOUT reward, outcome, policy performance, and
trading performance were not inspected. The historical exact working-tree
state during the original final generation remains NOT INDEPENDENTLY PROVABLE.

Files:

- `reproduction_audit.json`: machine-readable audit summary.
- `file_comparison.json`: size and SHA256 comparison for every compared file.
- `sha256.json`: hashes for this audit archive, excluding itself.
