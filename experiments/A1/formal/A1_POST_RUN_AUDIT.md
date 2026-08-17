# A1 Formal post-run audit

## Verdict

The official `A1_no_online_adaptation_2024H1` result passes the final read-only
audit. The preserved official Memory lineage is
`20260817T132343821395Z_11ae1ce4`; its final operational continuation is
`20260817T221009081674Z_11ae1ce4`.

The final population is AAPL 26/26, AMZN 26/26, and JPM 26/26, for 78/78 total,
with zero failures. The 78 decision records have 78 source-audit files and no
point-in-time violations.

## Recovery boundary and lineage

After reauthentication, the original process was found alive and had continued
past the previously observed 54/78 point. It reached a clean stopped boundary
of AAPL 26, AMZN 26, and JPM 17 (69 total). The last committed case was
`JPM:2024-04-26`; the first unresolved case was `JPM:2024-05-03`. That case was
classified `CLEAN_UNSTARTED`: no torn side effect existed, no rollback was
required, and exact pre-state proof was therefore not applicable.

The same lineage was resumed with `--resume`. No completed case was regenerated
or replaced, and no competing official trajectory was created.

## Correctness and treatment

- Final weekly XNYS decision sessions run from `2024-01-05` through `2024-06-28`.
- The frozen market horizon is `2024-07-05`; terminal `2024-06-28` credits
  mature on `2024-07-08` and correctly remain pending.
- Each symbol has 26 issued actions, 25 `ARCHIVED` credits, and one terminal
  `PENDING` credit.
- Every matured A1 credit is archived with reason
  `ONLINE_UPDATE_DISABLED_BY_ABLATION`.
- Initial and final policy SHA are
  `6baafc03b0b63512b3a66a1ae8f1ce1ce7e774395787626b49905e7b72cd1841`.
- Initial and final fast SHA are
  `365d06abf2d30f9ef3c283fb383712b3bc1b7439851e3c828f25e9dd676df2ec`.
- Optimiser steps, parameter-mutating updates, global mutations, and
  cross-symbol mutations are all zero.

## Archive integrity

The final run contains 1,735 files and 78 non-empty case directories. The
immutable remote bundle was copied through the encrypted versioned S3 bucket,
verified locally by SHA-256, and contains no `.env`. The machine-readable
inventory, resource accounting, audit, and research-freeze records are adjacent
to this document; `SHA256SUMS` is the final archive inventory.

The archive contains no AWS or DeepSeek credential material. AWS login attempts
are recorded as operational events only and are not counted as Formal cases.
The canonical `g5.xlarge` is stopped, persistent EBS is preserved, and the
running/pending AlphaMAS GPU count is zero.
