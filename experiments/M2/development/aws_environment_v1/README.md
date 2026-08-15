# AlphaMAS M2 AWS Environment v1

**PRE-FORMAL DEVELOPMENT — NOT FORMAL M2**

This archive records the M2-05 Retry #2 verification of the existing AWS GPU
environment. It contains no research dataset, credentials, account identifier,
private network address, or paid-model output.

The verified runtime source was AlphaMAS commit
`1594ef850999ecb29f150cb4a8eedfe20c6ad7a6`; the frozen experiments source was
`6c9e18d7d0ea1a2b91fd4ac5eefe829160a15cac`. All required Linux regressions,
A10G CUDA tensor smoke, S3 smoke, and persistent-EBS smoke passed. EC2 was
confirmed stopped after verification.

Torch in `gpu_smoke.json` is a hardware-smoke dependency only. It is not the
frozen M2 training framework.
