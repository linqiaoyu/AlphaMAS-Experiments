# M2 final pre-Formal environment archive

This archive completes M2-14 and binds M2-15 to the already-frozen architecture,
research identities, eight existing E2E trajectories, corrected authority audit,
delayed-credit audit, safe-resume audit, and A1/A2 preregistration.

The Retry #3 historical blocked audit remains unchanged in
`../e2e_pilot_v1/retry3_blocked_audit.json`.  Its over-strict interpretation is
superseded by `retry3_authority_audit_erratum.json`; it was not rewritten or
deleted.  ARR and AEMD are reclassified as correctness-valid because the M2
Actor owns only the Trader-slot handoff and the unchanged Portfolio Manager owns
the final policy decision.

No Agent trajectory was rerun.  This resolution made no DeepSeek, Qwen, AWS,
GPU, live market-data, or raw FinMultiTime call.  The raw trajectory bundle
remained on stopped EBS and was not reopened.  The source freeze is
`docs/m2/M2_PREFORMAL_ENVIRONMENT_FREEZE.md` with machine-readable equivalent
`docs/m2/m2_preformal_environment_freeze.json`.
