# Frozen M1 FinMultiTime input bundle

This directory contains the deterministic, point-in-time-safe FinMultiTime augmentation inputs for M1. It contains 78 standalone Evidence Packets for AAPL, AMZN, and JPM for the frozen 2024H1 weekly schedule.

The augmentation is additive: M0 historical-safe evidence remains a separate runtime input and is not copied into these packets. TEXT, TABLE, TIME_SERIES, and IMAGE are always explicit, including UNAVAILABLE states. The two formal images and their frozen Qwen captions are reused exactly; no Qwen model weights or raw upstream dataset are included.

M2, A1, and A2 must reuse these exact files and caption identities. They must not reclean, reselect, regenerate captions, change packet text, or rebuild from upstream FinMultiTime. No Agent, DeepSeek call, formal M1 run, or formal result is represented here.
