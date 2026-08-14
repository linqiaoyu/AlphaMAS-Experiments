# M1 FinMultiTime formal result

This directory contains the corrected, frozen M1 FinMultiTime input bundle and
the publicly archived Formal M1 result. The frozen inputs are under `inputs/`;
the source-integrity erratum is documented in
[M1_INPUT_CORRECTNESS_ERRATUM.md](M1_INPUT_CORRECTNESS_ERRATUM.md).

Formal M1 completed successfully and passed the post-run audit. The official
result is archived at
[`formal/runs/20260814T015553499023Z_ac0d1b00/`](formal/runs/20260814T015553499023Z_ac0d1b00/),
with its complete wrapper, analysis-ready tables, benchmarks, final Memory,
DecisionCache provenance, runtime Memory provenance, startup-interruption
provenance, audit reports, and checksum inventory.

The successful wrapper is the legal resume lineage of
`20260814T012538152812Z_ac0d1b00` through
`20260814T014003575028Z_ac0d1b00`. The two startup interruptions are preserved
as provenance only and are not competing formal result trajectories.

This Formal M1 result is research-frozen. Do not reclean the upstream
FinMultiTime dataset, regenerate captions, alter packet text, rerun or resume
the M1 wrapper, change the frozen inputs or M0 snapshot, or start M2/RL work
under this archive.
