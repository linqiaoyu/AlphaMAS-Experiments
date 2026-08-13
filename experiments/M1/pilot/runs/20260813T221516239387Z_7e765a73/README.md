# M1 real-Agent pilot attempt — blocked and preserved

**PILOT ATTEMPT PRESERVED**

**NOT AN OFFICIAL SUCCESSFUL PILOT**

**NOT FORMAL M1 RESULT**

**NOT USED FOR PERFORMANCE CLAIMS**

This is the first canonical four-case real-Agent attempt under the frozen M1
PILOT evidence bundle. All four chronological Agent decisions completed, but
the runner failed during final Memory-artifact publication before the complete
backtest result bundle could be written.

The failure is preserved exactly for a separate correctness review. No source
patch, resume, competing run, prompt change, evidence change, Formal M1 run,
Qwen call, raw FinMultiTime access, or AWS resource was started after the
failure.

Failure:

`ValueError: cannot archive complete final experiment Memory: AAPL:
FileNotFoundError` — the runtime Memory file was created under the
FinMultiTime-scoped namespace, while the archive helper searched the
pre-M1 namespace.

See `failure_manifest.json` for frozen identities and per-case validation.
