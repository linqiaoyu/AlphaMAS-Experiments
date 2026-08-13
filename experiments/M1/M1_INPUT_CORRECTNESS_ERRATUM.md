# M1 input correctness erratum

This archive supersedes the earlier M1 input freeze at archive commit
`4feb0a1e29143e04d64306505b49d3393b6c8b9d`; its verification commit was
`dbcfb4f02f73ec3f499c944b9b04c74129ddbf9e`. Both remain in Git history. The
correction was completed before Formal M1 and no Formal M1 result is
represented here.

## Correction

The pre-formal source-integrity audit found clustered headline/URL/body
corruption in the raw AAPL FinMultiTime news member. Under the fail-closed
policy, AAPL TEXT is unavailable for all 26 formal cases. AMZN retains its
source-native TEXT selection, and JPM remains unavailable because its news
member is absent. No article was fetched, replaced, or cross-filled.

The corrected contract is `M1-FINMULTITIME-v1.0.2`, superseding
`M1-FINMULTITIME-v1.0.1`. The contract and source correction are recorded in
the AlphaMAS source repository at commit
`a5ba0ea439fa5ef635ed64be138a5db91a119509`; the final bundle-manifest
documentation is at `7b905ed4d0b756dd5faff9f3a3ac7d00c50560a8`.

## Corrected bundle

- 78 cases and 78 JSON/text Evidence Packets.
- TEXT: 2 available cases and 76 unavailable cases.
- TABLE: 78 available; TIME_SERIES: 78 available.
- IMAGE: 52 available with frozen captions and 26 unavailable.
- PIT violations: 0; future-field violations: 0.
- Deterministic packet build: JSON mismatches 0, text mismatches 0.
- Qwen inference during correction: 0; canonical caption and image hashes unchanged.
- Formal M1 run: no.

The authoritative audit and equivalence records are under
`experiments/M1/provenance/`. The previous archive remains recoverable
through Git history; this commit replaces the working-tree input bundle and
removes the stale empty `evidence_packets/AAPL 2` directory.
