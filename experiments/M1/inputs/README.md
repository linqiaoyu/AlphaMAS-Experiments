# Frozen M1 FinMultiTime input bundle

This directory is the complete experiment-specific FinMultiTime augmentation input bundle for M1. It contains the frozen processed subset and 78 standalone Evidence Packets for AAPL, AMZN, and JPM on the frozen 2024H1 weekly decision schedule.

M1 is augmentation-not-replacement: M0 historical-safe evidence remains a separate runtime input and is not copied into a FinMultiTime packet. Every packet contains explicit `TEXT`, `TABLE`, `TIME_SERIES`, and `IMAGE` sections, including `UNAVAILABLE` states. TEXT is available for 4 cases and unavailable for 74; images/captions are generated for 52 cases and not applicable for 26.

The two original formal images and the two frozen Qwen captions were generated once and are reused by identity. The 16 GB upstream FinMultiTime dataset and the 4.26 GB Qwen model weights are intentionally not duplicated here.

M2, A1, and A2 must reuse these exact frozen M1 input files and caption identities. They must not reclean, reselect, regenerate captions, change packet text, or rebuild from upstream FinMultiTime. If a future correctness issue is found, stop and review the freeze before changing anything.

No Agent, DeepSeek call, formal M1 run, M1 pilot, performance result, or formal M1 output is represented by this bundle. M1 runtime integration is not frozen yet.

## Verification

From this directory, validate the complete bundle with:

```bash
python3 - <<'PY'
import hashlib, json
from pathlib import Path

root = Path('.')
inventory = json.loads((root / 'manifests/input_bundle_checksums.json').read_text())
failures = []
for item in inventory['files']:
    path = root / item['path']
    if not path.is_file() or hashlib.sha256(path.read_bytes()).hexdigest() != item['sha256']:
        failures.append(item['path'])
assert not failures, failures
assert len(list((root / 'evidence_packets').glob('*/*.json'))) == 78
assert len(list((root / 'evidence_packets').glob('*/*.txt'))) == 78
print('M1 input bundle verification passed')
PY
```

The canonical packet manifest, input-bundle manifest, checksum inventory, provenance, and validation reports are all included for independent inspection.
