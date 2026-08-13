# M1 input archive verification

Verdict: `PASS`

- Archive: `AlphaMAS-Experiments/experiments/M1/inputs/`
- Remote source: `https://github.com/linqiaoyu/AlphaMAS-Experiments.git`
- Verified remote commit: `3750fa50224ba46ab1d4bf5511cb5e8fa514445b`
- Verification method: fresh temporary clone of the remote repository, checked out at the verified commit
- Tracked input files: `252`
- Input bundle bytes: `4,398,808`
- Checksum inventory entries: `251`
- Checksum failures: `0`
- JSON files parsed: `171`
- CSV files parsed: `0`
- Final Evidence Packets: `78` JSON + `78` text representations
- Images: `2`
- Frozen caption artefacts: `2`
- Caption status mapping: `GENERATED=52`, `NOT_APPLICABLE=26`, `PENDING=0`
- Packet validation: `PASS`
- Secret/credential scan: `PASS`
- Private machine-path scan: `PASS`
- Raw upstream FinMultiTime dataset archived: `NO`
- Qwen model weights archived: `NO`
- Formal M1 run represented: `NO`

The fresh clone is the archival source-of-truth verification. M0 archive contents were not modified by this commit or the preceding M1 input commits. The previous M1 freeze (`4feb0a1e29143e04d64306505b49d3393b6c8b9d`) and verification commit (`dbcfb4f02f73ec3f499c944b9b04c74129ddbf9e`) remain in history and are superseded before Formal M1.
