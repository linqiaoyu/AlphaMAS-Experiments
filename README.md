# AlphaMAS Experiments

Public reproducibility archive for AlphaMAS dissertation experiments. The source repository contains code, algorithms, configs, and runners; this repository contains frozen experiment inputs, outputs, intermediate artefacts, metrics, validation, provenance, and analysis-ready data.

Public archive: [AlphaMAS-Experiments](https://github.com/linqiaoyu/AlphaMAS-Experiments)

Complete upstream datasets are not mirrored here. Only experiment-specific frozen inputs and processed artefacts belong in this repository.

## Experiments

- [Formal M0](experiments/M0/README.md): `M0_original_prompt_2024H1`
- [Corrected pre-formal M1 inputs](experiments/M1/README.md): FinMultiTime 78-case input freeze; Formal M1 not run

The directory layout is reusable for future `M1`, `M2`, and `M3` experiments. The M1 directory contains only the corrected pre-formal input bundle and provenance; it does not contain a Formal M1 result.

## Reproducibility

The M0 archive is self-contained after cloning this repository and downloading no live data or calling DeepSeek. See the M0 README for the exact frozen source commit, run lineage, archive checksum, and extraction instructions.

This repository contains no API keys, credentials, `.env` files, authentication headers, or private source datasets.
