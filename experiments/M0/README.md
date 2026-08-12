# Formal M0 archive

Experiment ID: `M0_original_prompt_2024H1`

Public archive: [Formal M0 on GitHub](https://github.com/linqiaoyu/AlphaMAS-Experiments/tree/main/experiments/M0)

This is the public, research-frozen archive of the completed Formal M0 run. It was built by read-only analysis of the frozen artefacts in `AlphaMAS` at source branch `baseline-m0`, commit `2535896c8b1070b19c06fa6a936663babb4356f7`.

## Identity

- Successful run: `20260812T082530978211Z_2535896c`
- Original interrupted lineage: `20260811T210814251902Z_2535896c`
- Graph config SHA256: `5b1b6e1c132c13f9830b377ba9d54bf0c792b087e9917af5f0ada9cc895d661e`
- Backtest protocol SHA256: `bb08f3e169d32ff44a40988933fd8e58638596f5a1a04f3d0e1e22d8e4b116d7`
- AAPL snapshot: `5428fc2c672f3b68c7c3e83b4a22bd5b7330c95a8b4194695762539d9d8a5af3`
- AMZN snapshot: `c4b5c747d75ba658c6f6833348783e3f8a8c571380c930de20cf9fb7dd6b1444`
- JPM snapshot: `74cf77b77b0a83ce8e6246578d4da30bf7622558e8973bda71344b99b9dfd6fc`
- SPY snapshot: `22e6996ebf963787f40d54bfc59e1ca088fa698cb82b639768504dbdbb2d25ac`

The official validation passed with AAPL 26/26, AMZN 26/26, JPM 26/26, total 78/78, unresolved failures 0, complete agent cases, and complete immutable Memory archives.

## Contents

- `inputs/`: experiment-specific market snapshots, corporate actions, and input manifest.
- `provenance/`: resolved configs, environment, schema, schedule, source config, dependency lockfile, and both lineage run manifests.
- `agent_outputs/`: the complete raw immutable bundle.
- `memory/`: final Memory Markdown and manifest.
- `trading/`: decisions, orders, fills, daily equity, corporate actions, and metrics.
- `benchmarks/`: individual Buy & Hold and SPY outputs, plus the derived equal-weight Buy & Hold benchmark.
- `aggregate/`: equal-weight M0 equity and metrics.
- `analysis_ready/`: formal bundle analysis tables.
- `analysis/`: post-run decision, outcome, source-availability, and Memory audits.
- `cost/`: exact provider-usage cost audit by case, stock, and agent role.
- `validation/`: official validation report and failure ledger.
- `M0_POSTRUN_AUDIT.md` and `M0_POSTRUN_AUDIT.json`: the formal post-run report.
- `tools/build_m0_archive.py`: the read-only derived-analysis builder used to produce the post-run artefacts.

## Complete raw bundle

`agent_outputs/formal_m0_complete_bundle.tar.gz` contains the complete original and resumed `AlphaMAS` Formal M0 experiment tree, including all 78 case artefacts, runtime DecisionCache, frozen inputs, agent outputs, Memory, trading outputs, benchmarks, analysis-ready artefacts, and validation. It deliberately does not mirror an unrelated full upstream dataset.

Verify it with:

```sh
shasum -a 256 -c SHA256SUMS
tar -tzf agent_outputs/formal_m0_complete_bundle.tar.gz >/dev/null
```

To extract a local copy without invoking the runner:

```sh
mkdir -p /tmp/alphamas-m0-extracted
tar -xzf agent_outputs/formal_m0_complete_bundle.tar.gz -C /tmp/alphamas-m0-extracted
```

## Research integrity

The audit made zero new LLM calls and zero new paid API calls. It did not rerun M0, resume M0, use `--force`, start M1, process FinMultiTime, run Qwen/VLM, start Agentic RL, or run M2/M3.
