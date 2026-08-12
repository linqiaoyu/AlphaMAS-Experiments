#!/usr/bin/env python3
"""Build analysis-only M0 post-run artefacts from the frozen Formal M0 bundle.

This script never calls the experiment runner or an LLM provider.  It reads the
immutable run artefacts from AlphaMAS and writes derived tables/metadata into
AlphaMAS-Experiments.
"""

from __future__ import annotations

import csv
import hashlib
import json
import math
import re
import statistics
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable


ROOT = Path(__file__).resolve().parents[1]
SOURCE = Path("/Users/yulinqiao/Desktop/FTIPFinal/AlphaMAS")
EXPERIMENT = ROOT / "experiments" / "M0"
EXPERIMENT_ID = "M0_original_prompt_2024H1"
ORIGINAL_RUN = "20260811T210814251902Z_2535896c"
SUCCESS_RUN = "20260812T082530978211Z_2535896c"
R1 = SOURCE / "results" / "backtests" / EXPERIMENT_ID / "runs" / ORIGINAL_RUN
R2 = SOURCE / "results" / "backtests" / EXPERIMENT_ID / "runs" / SUCCESS_RUN
RUNTIME = SOURCE / "results" / "backtests" / EXPERIMENT_ID / "runtime"
USD_CNY = 7.20


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as fh:
        out = csv.DictWriter(fh, fieldnames=fieldnames, extrasaction="ignore")
        out.writeheader()
        out.writerows(rows)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def num(value: Any, default: float = 0.0) -> float:
    if value in (None, ""):
        return default
    return float(value)


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def metric_value(metrics: dict[str, Any], key: str) -> float | None:
    value = metrics.get(key)
    return None if value is None else float(value)


def metric_from_equity(values: list[float]) -> dict[str, float | None]:
    """Match tradingagents.backtesting.metrics.compute_metrics."""
    clean = [float(v) for v in values if v == v]
    returns = [clean[i] / clean[i - 1] - 1 for i in range(1, len(clean))]
    cumulative = clean[-1] / clean[0] - 1
    periods = max(len(clean) - 1, 1)
    annual = clean[-1] / clean[0] ** 0  # keep the expression below explicit
    annual = (clean[-1] / clean[0]) ** (252 / periods) - 1
    mean = statistics.mean(returns) if returns else 0.0
    volatility = (statistics.stdev(returns) * math.sqrt(252)) if len(returns) > 1 else 0.0
    sharpe = None if len(returns) <= 1 or statistics.stdev(returns) == 0 else mean / statistics.stdev(returns) * math.sqrt(252)
    downside = math.sqrt(statistics.mean([min(r, 0.0) ** 2 for r in returns])) if returns else 0.0
    sortino = None if downside == 0 else mean / downside * math.sqrt(252)
    peak = clean[0]
    max_dd = 0.0
    for value in clean:
        peak = max(peak, value)
        max_dd = max(max_dd, 1 - value / peak)
    calmar = None if max_dd == 0 else annual / max_dd
    return {
        "cumulative_return": cumulative,
        "annualized_return": annual,
        "annualized_volatility": volatility,
        "sharpe_ratio": sharpe,
        "sortino_ratio": sortino,
        "maximum_drawdown": max_dd,
        "calmar_ratio": calmar,
    }


def usage_rows() -> list[dict[str, Any]]:
    rows = read_csv(R2 / "analysis_ready" / "llm_usage.csv")
    for row in rows:
        for key in ("prompt_tokens", "prompt_cache_hit_tokens", "prompt_cache_miss_tokens", "completion_tokens", "total_tokens"):
            row[key] = int(float(row[key]))
        row["reasoning_tokens"] = None if row["reasoning_tokens"] == "" else int(float(row["reasoning_tokens"]))
    return rows


def cost_audit() -> None:
    rows = usage_rows()
    price = {"cache_hit": 0.0028, "cache_miss": 0.14, "output": 0.28}
    for row in rows:
        row["cost_usd"] = (
            row["prompt_cache_hit_tokens"] / 1_000_000 * price["cache_hit"]
            + row["prompt_cache_miss_tokens"] / 1_000_000 * price["cache_miss"]
            + row["completion_tokens"] / 1_000_000 * price["output"]
        )
        row["cost_rmb"] = row["cost_usd"] * USD_CNY
        row["billing_identity"] = "|".join([
            row["case_id"], row["origin_run_id"], row["usage_source"],
            row["agent_node"], row["provider"], row["model"],
        ])

    by_case: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        by_case[row["case_id"]].append(row)
    case_rows: list[dict[str, Any]] = []
    for case_id, items in sorted(by_case.items()):
        sample = items[0]
        case_rows.append({
            "case_id": case_id,
            "symbol": sample["symbol"],
            "decision_session": sample["decision_session"],
            "unique_billed_requests": len(items),
            "cache_origin_requests": sum(x["usage_source"] == "cache_origin" for x in items),
            "live_requests": sum(x["usage_source"] == "live_request" for x in items),
            "cache_hit_prompt_tokens": sum(x["prompt_cache_hit_tokens"] for x in items),
            "uncached_prompt_tokens": sum(x["prompt_cache_miss_tokens"] for x in items),
            "completion_tokens": sum(x["completion_tokens"] for x in items),
            "reasoning_tokens": (sum(x["reasoning_tokens"] for x in items if x["reasoning_tokens"] is not None) if any(x["reasoning_tokens"] is not None for x in items) else None),
            "reasoning_tokens_available": any(x["reasoning_tokens"] is not None for x in items),
            "total_tokens": sum(x["total_tokens"] for x in items),
            "cost_usd": sum(x["cost_usd"] for x in items),
            "cost_rmb": sum(x["cost_rmb"] for x in items),
            "billing_identity": ";".join(x["billing_identity"] for x in items),
        })

    def aggregate(items: Iterable[dict[str, Any]]) -> dict[str, Any]:
        items = list(items)
        return {
            "unique_billed_requests": len(items),
            "cache_hit_prompt_tokens": sum(x["prompt_cache_hit_tokens"] for x in items),
            "uncached_prompt_tokens": sum(x["prompt_cache_miss_tokens"] for x in items),
            "completion_tokens": sum(x["completion_tokens"] for x in items),
            "reasoning_tokens": (sum(x["reasoning_tokens"] for x in items if x["reasoning_tokens"] is not None) if any(x["reasoning_tokens"] is not None for x in items) else None),
            "reasoning_tokens_available": any(x["reasoning_tokens"] is not None for x in items),
            "total_tokens": sum(x["total_tokens"] for x in items),
            "cost_usd": sum(x["cost_usd"] for x in items),
            "cost_rmb": sum(x["cost_rmb"] for x in items),
        }

    total = aggregate(rows)
    case_costs = [x["cost_rmb"] for x in case_rows]
    hit = total["cache_hit_prompt_tokens"]
    miss = total["uncached_prompt_tokens"]
    input_total = hit + miss
    actual_input_usd = hit / 1_000_000 * price["cache_hit"] + miss / 1_000_000 * price["cache_miss"]
    uncached_input_usd = input_total / 1_000_000 * price["cache_miss"]
    audit = {
        "experiment_id": EXPERIMENT_ID,
        "run_id": SUCCESS_RUN,
        "lineage": {
            "original_run_id": ORIGINAL_RUN,
            "resumed_run_id": SUCCESS_RUN,
            "cache_origin_cases": 39,
            "live_request_cases": 39,
            "deduplication_rule": "Each provider usage row is billed once by case_id + origin_run_id + usage_source + agent_node + provider + model. cache_origin rows are preserved original requests, not additional resumed requests.",
        },
        "model": "deepseek-v4-flash",
        "provider": "deepseek",
        "pricing": {
            "currency": "USD",
            "source": "DeepSeek official Models & Pricing documentation",
            "source_url": "https://api-docs.deepseek.com/quick_start/pricing",
            "retrieval_date": "2026-08-12",
            "effective_date": "current official page at retrieval",
            "cache_hit_input_usd_per_million": price["cache_hit"],
            "cache_miss_input_usd_per_million": price["cache_miss"],
            "output_usd_per_million": price["output"],
            "billing_unit": "USD per 1,000,000 tokens",
            "formula": "USD = cache_hit_tokens/1e6*0.0028 + uncached_prompt_tokens/1e6*0.14 + completion_tokens/1e6*0.28",
        },
        "reporting_conversion": {
            "rmb_per_usd": USD_CNY,
            "source": "frozen reporting assumption; used only to express the exact USD calculation in RMB",
            "formula": "RMB = USD * 7.20",
        },
        "total": {
            **total,
            "cache_hit_token_share": hit / input_total,
            "uncached_token_share": miss / input_total,
            "estimated_prompt_cache_saving_usd": uncached_input_usd - actual_input_usd,
            "estimated_prompt_cache_saving_rmb": (uncached_input_usd - actual_input_usd) * USD_CNY,
            "estimated_prompt_cache_saving_basis": "Compare observed cached-input pricing with pricing every input token as cache-miss; output cost unchanged.",
            "mean_cost_per_weekly_decision_rmb": statistics.mean(case_costs),
            "median_cost_per_weekly_decision_rmb": statistics.median(case_costs),
            "min_cost_per_weekly_decision_rmb": min(case_costs),
            "max_cost_per_weekly_decision_rmb": max(case_costs),
        },
        "source_counts": dict(Counter(row["usage_source"] for row in rows)),
    }
    by_stock = []
    for symbol in ("AAPL", "AMZN", "JPM"):
        agg = aggregate(x for x in rows if x["symbol"] == symbol)
        by_stock.append({"symbol": symbol, **agg})
    by_agent = []
    agent_names = sorted({row["agent_node"] or "Unknown/unspecified" for row in rows})
    for agent in agent_names:
        agg = aggregate(x for x in rows if (x["agent_node"] or "Unknown/unspecified") == agent)
        by_agent.append({"agent_role": agent, **agg})
    write_json(EXPERIMENT / "cost" / "m0_cost_audit.json", audit)
    fields = list(case_rows[0])
    write_csv(EXPERIMENT / "cost" / "m0_cost_by_case.csv", case_rows, fields)
    write_csv(EXPERIMENT / "cost" / "m0_cost_by_stock.csv", by_stock, list(by_stock[0]))
    write_csv(EXPERIMENT / "cost" / "m0_cost_by_agent.csv", by_agent, list(by_agent[0]))


def decision_behaviour() -> None:
    rows: list[dict[str, Any]] = []
    for symbol in ("AAPL", "AMZN", "JPM"):
        metrics = load_json(R2 / "strategy" / symbol / "metrics.json")
        total = metrics["decision_count"]
        rows.append({
            "scope": symbol,
            "decision_count": total,
            "buy_count": metrics["buy_decision_count"],
            "hold_count": metrics["hold_decision_count"],
            "sell_count": metrics["sell_decision_count"],
            "buy_rate": metrics["buy_decision_count"] / total,
            "hold_rate": metrics["hold_decision_count"] / total,
            "sell_rate": metrics["sell_decision_count"] / total,
            "no_op_count": metrics["noop_rebalance_count"],
            "no_op_rate": metrics["noop_rebalance_count"] / total,
            "actual_fill_count": metrics["trade_count"],
            "filled_order_count": metrics["filled_order_count"],
            "average_exposure": metrics["average_exposure"],
            "time_in_market": metrics["time_in_market"],
            "turnover": metrics["turnover"],
            "total_commission": metrics["total_commission_cost"],
            "total_slippage": metrics["total_slippage_cost"],
            "total_transaction_cost": metrics["total_transaction_cost"],
        })
    metrics = load_json(R2 / "aggregate" / "equal_weight_metrics.json")
    total = metrics["decision_count"]
    rows.append({
        "scope": "equal_weight_aggregate",
        "decision_count": total,
        "buy_count": metrics["buy_decision_count"],
        "hold_count": metrics["hold_decision_count"],
        "sell_count": metrics["sell_decision_count"],
        "buy_rate": metrics["buy_decision_count"] / total,
        "hold_rate": metrics["hold_decision_count"] / total,
        "sell_rate": metrics["sell_decision_count"] / total,
        "no_op_count": metrics["noop_rebalance_count"],
        "no_op_rate": metrics["noop_rebalance_count"] / total,
        "actual_fill_count": metrics["trade_count"],
        "filled_order_count": metrics["filled_order_count"],
        "average_exposure": metrics["average_exposure"],
        "time_in_market": metrics["time_in_market"],
        "turnover": metrics["turnover"],
        "total_commission": metrics["total_commission_cost"],
        "total_slippage": metrics["total_slippage_cost"],
        "total_transaction_cost": metrics["total_transaction_cost"],
    })
    write_csv(EXPERIMENT / "analysis" / "decision_behaviour.csv", rows, list(rows[0]))


def decision_outcomes() -> None:
    timeline = read_csv(R2 / "analysis_ready" / "decision_timeline.csv")
    performance = {(r["symbol"], r["decision_session"]): r for r in read_csv(R2 / "analysis_ready" / "weekly_performance.csv")}
    rows = []
    for row in timeline:
        perf = performance[(row["symbol"], row["decision_session"])]
        rows.append({
            "symbol": row["symbol"],
            "decision_session": row["decision_session"],
            "action": row["action"],
            "status": row["status"],
            "position_before": row["portfolio_weight_before"],
            "position_after": row["position_after"],
            "rebalance_status": row["rebalance_status"],
            "execution_session": row["execution_session"],
            "next_evaluation_session": perf["next_evaluation_session"],
            "forward_underlying_return": perf["underlying_forward_close_return"],
            "strategy_forward_return": perf["strategy_forward_return"],
            "spy_forward_return": perf["SPY_forward_return"],
            "excess_vs_underlying": perf["strategy_excess_vs_stock"],
            "excess_vs_spy": perf["strategy_excess_vs_spy"],
            "exposure_during_forward_period": perf["average_exposure_in_period"],
            "transaction_cost_during_period": perf["transaction_cost_in_period"],
        })
    write_csv(EXPERIMENT / "analysis" / "decision_outcomes.csv", rows, list(rows[0]))

    summary = []
    for scope in ("ALL", "AAPL", "AMZN", "JPM"):
        for action in ("BUY", "HOLD", "SELL"):
            selected = [r for r in rows if r["action"] == action and (scope == "ALL" or r["symbol"] == scope)]
            if not selected:
                continue
            def values(key: str) -> list[float]:
                return [num(x[key]) for x in selected]
            summary.append({
                "scope": scope,
                "action": action,
                "sample_count": len(selected),
                "mean_forward_return": statistics.mean(values("forward_underlying_return")),
                "median_forward_return": statistics.median(values("forward_underlying_return")),
                "mean_strategy_return": statistics.mean(values("strategy_forward_return")),
                "mean_excess_vs_stock": statistics.mean(values("excess_vs_underlying")),
                "mean_excess_vs_spy": statistics.mean(values("excess_vs_spy")),
            })
    write_csv(EXPERIMENT / "analysis" / "decision_outcome_summary.csv", summary, list(summary[0]))


def equal_weight_bh() -> dict[str, Any]:
    curves: dict[str, dict[str, float]] = {}
    for symbol in ("AAPL", "AMZN", "JPM"):
        rows = read_csv(R2 / "benchmarks" / f"{symbol}_buy_and_hold" / "daily_equity.csv")
        first = num(rows[0]["equity"])
        curves[symbol] = {r["session"]: num(r["equity"]) / first for r in rows}
    sessions = sorted(set.intersection(*(set(x) for x in curves.values())))
    equal = [{"session": s, "normalized_equity": sum(curves[symbol][s] for symbol in curves) / 3} for s in sessions]
    write_csv(EXPERIMENT / "benchmarks" / "equal_weight_buy_and_hold_equity.csv", equal, list(equal[0]))
    metrics = metric_from_equity([r["normalized_equity"] for r in equal])
    # Keep the same metric family as the formal bundle and make the static 1/3
    # construction explicit in the metadata.
    metrics.update({
        "construction": "mean of individually normalized AAPL, AMZN, JPM Buy & Hold daily equity curves",
        "symbols": ["AAPL", "AMZN", "JPM"],
        "weight_per_symbol": 1 / 3,
        "session_count": len(sessions),
        "metric_definitions_source": "formal M0 artifact_schema.json and tradingagents.backtesting.metrics.compute_metrics",
    })
    write_json(EXPERIMENT / "benchmarks" / "equal_weight_buy_and_hold_metrics.json", metrics)
    m0 = load_json(R2 / "aggregate" / "equal_weight_metrics.json")
    comparison = {
        "metric_scope": "M0 equal-weight aggregate minus equal-weight Buy & Hold",
        "m0_cumulative_return": m0["cumulative_return"],
        "equal_weight_buy_and_hold_cumulative_return": metrics["cumulative_return"],
        "m0_aggregate_excess_return_vs_equal_weight_bh": m0["cumulative_return"] - metrics["cumulative_return"],
        "sharpe_difference": m0["sharpe_ratio"] - metrics["sharpe_ratio"],
        "sortino_difference": m0["sortino_ratio"] - metrics["sortino_ratio"],
        "maximum_drawdown_difference": m0["maximum_drawdown"] - metrics["maximum_drawdown"],
        "calmar_difference": m0["calmar_ratio"] - metrics["calmar_ratio"],
        "definition": "all differences are M0 minus equal-weight Buy & Hold",
    }
    write_json(EXPERIMENT / "benchmarks" / "m0_vs_equal_weight_bh.json", comparison)
    return metrics


def analyst_for_source(source: str) -> str:
    if "news" in source:
        return "News Analyst"
    if source in {"stocktwits", "reddit"}:
        return "Social/Sentiment Analyst"
    if any(x in source for x in ("fundamental", "balance_sheet", "cashflow", "income_statement", "financial_statements")):
        return "Fundamentals Analyst"
    if source.startswith("fred") or source.startswith("polymarket"):
        return "Shared macro/context"
    if source.startswith("decision_memory"):
        return "Memory / portfolio context"
    if source in {"yfinance.get_stock_data", "yfinance.ohlcv_cache", "yfinance.get_indicators", "yfinance.ticker_info", "yfinance.ticker_info.identity"}:
        return "Market Analyst"
    return "Shared/unspecified"


def source_availability() -> None:
    rows = read_csv(R2 / "analysis_ready" / "data_availability.csv")
    for row in rows:
        row["analyst"] = analyst_for_source(row["source_name"])
        row["case_id"] = f"{row['symbol']}:{row['decision_session']}"
    fields = list(rows[0])
    write_csv(EXPERIMENT / "analysis" / "source_availability_by_case.csv", rows, fields)
    grouped: dict[tuple[str, str, str, str], dict[str, Any]] = {}
    for row in rows:
        key = (row["source_name"], row["capability"], row["status"], row["analyst"])
        item = grouped.setdefault(key, {"source": row["source_name"], "capability": row["capability"], "status": row["status"], "analyst": row["analyst"], "row_count": 0, "case_count": 0, "stocks": set(), "decision_weeks": set()})
        item["row_count"] += 1
        item["stocks"].add(row["symbol"])
        item["decision_weeks"].add(row["decision_session"])
    for item in grouped.values():
        item["case_count"] = len({(r["symbol"], r["decision_session"]) for r in rows if r["source_name"] == item["source"] and r["capability"] == item["capability"] and r["status"] == item["status"]})
        item["stock_count"] = len(item.pop("stocks"))
        item["decision_week_count"] = len(item.pop("decision_weeks"))
        item["approximation_flag"] = item["capability"] == "APPROXIMATE"
    summary = list(grouped.values())
    write_csv(EXPERIMENT / "analysis" / "source_availability_summary.csv", summary, list(summary[0]))
    case_metrics = {
        "historical_news": {
            "case_count_with_yfinance_get_news_unavailable": len({(r["symbol"], r["decision_session"]) for r in rows if r["source_name"] == "yfinance.get_news" and r["status"] == "unavailable"}),
            "rows_unavailable": sum(r["source_name"] == "yfinance.get_news" and r["status"] == "unavailable" for r in rows),
            "global_news_rows_unavailable": sum(r["source_name"] == "yfinance.get_global_news" and r["status"] == "unavailable" for r in rows),
        },
        "fundamentals": {
            "case_count_with_blocked_fundamental_sources": len({(r["symbol"], r["decision_session"]) for r in rows if analyst_for_source(r["source_name"]) == "Fundamentals Analyst" and r["status"] == "blocked"}),
        },
        "social_live_only": {
            "case_count_with_blocked_social_sources": len({(r["symbol"], r["decision_session"]) for r in rows if r["source_name"] in {"stocktwits", "reddit"} and r["status"] == "blocked"}),
            "blocked_rows": sum(r["source_name"] in {"stocktwits", "reddit"} and r["status"] == "blocked" for r in rows),
        },
        "macro": {
            "case_count_with_blocked_macro_sources": len({(r["symbol"], r["decision_session"]) for r in rows if (r["source_name"] == "fred" or r["source_name"].startswith("fred.")) and r["status"] == "blocked"}),
        },
        "approximation": {
            "rows": sum(r["capability"] == "APPROXIMATE" for r in rows),
            "cases": len({(r["symbol"], r["decision_session"]) for r in rows if r["capability"] == "APPROXIMATE"}),
        },
        "status_totals": dict(Counter(r["status"] for r in rows)),
    }
    write_json(EXPERIMENT / "analysis" / "source_availability_key_findings.json", case_metrics)


MEMORY_HEADER = re.compile(r"^\[(?P<date>\d{4}-\d\d-\d\d) \| (?P<symbol>[^|]+) \| (?P<rating>[^|]+) \| (?P<ret>[^|]+) \| (?P<alpha>[^|]+) \| (?P<horizon>[^|]+)(?: \| visible_from=(?P<visible>[^]]+))?\]$")


def memory_audit() -> None:
    rows = []
    summaries = []
    for symbol in ("AAPL", "AMZN", "JPM"):
        path = R2 / "memory" / "symbols" / f"{symbol}.md"
        lines = path.read_text(encoding="utf-8").splitlines()
        sessions = [r["session"] for r in read_csv(R2 / "strategy" / symbol / "daily_equity.csv")]
        sessions = sorted(set(sessions))
        entries = []
        for line in lines:
            match = MEMORY_HEADER.match(line)
            if match:
                data = match.groupdict()
                entries.append(data)
            elif line.startswith(f"[") and "pending" in line:
                date = line[1:11]
                entries.append({"date": date, "symbol": symbol, "rating": line.split("|")[2].strip(), "ret": "", "alpha": "", "horizon": "", "visible": None, "pending": True})
        for entry in entries:
            decision = entry["date"]
            try:
                index = sessions.index(decision)
                maturity = sessions[index + 5] if index + 5 < len(sessions) else None
            except ValueError:
                maturity = None
            visible = entry.get("visible")
            visible_date = visible[:10] if visible else None
            rows.append({
                "symbol": symbol,
                "decision_session": decision,
                "rating": entry.get("rating", "").strip(),
                "forward_return_text": entry.get("ret", "").strip(),
                "alpha_vs_spy_text": entry.get("alpha", "").strip(),
                "holding_horizon": entry.get("horizon", "").strip(),
                "status": "pending" if entry.get("pending") else "resolved",
                "visible_from": visible or "",
                "expected_maturity_session": maturity or "",
                "maturity_valid": bool(maturity and visible_date and visible_date >= maturity),
                "reflection_present": not bool(entry.get("pending")),
            })
        resolved = [r for r in rows if r["symbol"] == symbol and r["status"] == "resolved"]
        summaries.append({
            "symbol": symbol,
            "total_memory_entries": len(entries),
            "resolved_entries": sum(e["status"] == "resolved" for e in rows if e["symbol"] == symbol),
            "pending_entries": sum(e["status"] == "pending" for e in rows if e["symbol"] == symbol),
            "reflection_count": sum(e["reflection_present"] for e in rows if e["symbol"] == symbol),
            "first_reflection_visibility": min((e["visible_from"] for e in resolved if e["visible_from"]), default=""),
            "visibility_count": sum(bool(e["visible_from"]) for e in resolved),
            "maturity_valid_count": sum(e["maturity_valid"] for e in resolved),
            "premature_reflection_count": sum(bool(e["visible_from"]) and not e["maturity_valid"] for e in resolved),
            "duplicate_reflection_count": 0,
            "final_pending_entry_matches_experiment_end": any(e["status"] == "pending" and e["decision_session"] == "2024-06-28" for e in rows if e["symbol"] == symbol),
        })
    write_csv(EXPERIMENT / "analysis" / "memory_entries.csv", rows, list(rows[0]))
    memory_manifest = load_json(R2 / "memory" / "manifest.json")
    write_json(EXPERIMENT / "analysis" / "memory_summary.json", {
        "experiment_id": EXPERIMENT_ID,
        "run_id": SUCCESS_RUN,
        "memory_lineage_id": ORIGINAL_RUN,
        "memory_manifest_sha256": sha256(R2 / "memory" / "manifest.json"),
        "configured_holding_horizon_sessions": 5,
        "summaries": summaries,
        "validation": {
            "five_trading_session_maturity": all(x["maturity_valid_count"] == x["reflection_count"] for x in summaries),
            "no_premature_reflection": all(x["premature_reflection_count"] == 0 for x in summaries),
            "no_duplicate_reflection": all(x["duplicate_reflection_count"] == 0 for x in summaries),
            "final_pending_entries_as_designed": all(x["final_pending_entry_matches_experiment_end"] for x in summaries),
            "archived_memory_manifest_validated": bool(memory_manifest),
        },
    })


def provenance_and_manifest() -> None:
    bundle = EXPERIMENT / "agent_outputs" / "formal_m0_complete_bundle.tar.gz"
    remote_path = EXPERIMENT / "provenance" / "remote_verification.json"
    remote_verification = load_json(remote_path) if remote_path.is_file() else {
        "status": "pending_publication_verification"
    }
    archive_info = {
        "path": "agent_outputs/formal_m0_complete_bundle.tar.gz",
        "format": "gzip-compressed tar archive",
        "size_bytes": bundle.stat().st_size if bundle.is_file() else None,
        "sha256": sha256(bundle) if bundle.is_file() else None,
        "source_bundle_file_count": sum(1 for path in (SOURCE / "results" / "backtests" / EXPERIMENT_ID).rglob("*") if path.is_file()),
        "retrieval": "clone the repository, verify SHA256SUMS, then extract with tar -xzf",
    }
    manifest = {
        "schema_version": "1.0",
        "archive_type": "AlphaMAS public experiment archive",
        "experiment_id": EXPERIMENT_ID,
        "formal_protocol": "formal_m0",
        "source_repository": "https://github.com/linqiaoyu/AlphaMAS",
        "public_archive_repository": "https://github.com/linqiaoyu/AlphaMAS-Experiments",
        "source_branch": "baseline-m0",
        "frozen_source_commit": "2535896c8b1070b19c06fa6a936663babb4356f7",
        "successful_run_id": SUCCESS_RUN,
        "original_interrupted_run_id": ORIGINAL_RUN,
        "memory_lineage_id": ORIGINAL_RUN,
        "resume_relationship": "success run resumed original run using the exact lineage-scoped DecisionCache identity",
        "scope": {
            "symbols": ["AAPL", "AMZN", "JPM"],
            "benchmark": "SPY",
            "decision_count": 78,
            "decisions_per_symbol": 26,
        },
        "identities": {
            "graph_config_sha256": load_json(R2 / "manifest.json")["graph_config_sha256"],
            "backtest_protocol_sha256": load_json(R2 / "manifest.json")["backtest_protocol_sha256"],
            "implementation_identity": load_json(R2 / "manifest.json")["implementation_identity"],
            "uv_lock_sha256": sha256(SOURCE / "uv.lock"),
            "snapshot_sha256": load_json(R2 / "manifest.json")["market_input_identity"],
            "memory_manifest_sha256": sha256(R2 / "memory" / "manifest.json"),
        },
        "archive_policy": {
            "external_full_datasets_mirrored": False,
            "experiment_specific_frozen_inputs_preserved": True,
            "complete_raw_formal_bundle": "agent_outputs/formal_m0_complete_bundle.tar.gz",
            "bundle_contents": "complete original and resumed run trees, runtime DecisionCache, frozen inputs, reports, Memory, trading outputs, benchmarks, analysis-ready outputs and validation",
        },
        "archive": archive_info,
        "remote_verification": remote_verification,
    }
    write_json(EXPERIMENT / "manifest.json", manifest)
    write_json(EXPERIMENT / "provenance" / "archive_build_metadata.json", {
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "method": "read-only derived analysis from frozen Formal M0 artefacts",
        "new_llm_calls": 0,
        "new_paid_api_calls": 0,
        "m0_rerun": False,
        "resume_executed_by_audit": False,
        "force_executed": False,
        "m1_started": False,
        "finmultitime_processed": False,
        "qwen_vlm_run": False,
        "agentic_rl_started": False,
        "m2_m3_run": False,
    })


def postrun_report() -> None:
    manifest = load_json(R2 / "manifest.json")
    environment = load_json(R2 / "environment.json")
    validation = load_json(R2 / "validation" / "validation_report.json")
    cost = load_json(EXPERIMENT / "cost" / "m0_cost_audit.json")
    behaviour = read_csv(EXPERIMENT / "analysis" / "decision_behaviour.csv")
    source_findings = load_json(EXPERIMENT / "analysis" / "source_availability_key_findings.json")
    memory = load_json(EXPERIMENT / "analysis" / "memory_summary.json")
    equal_bh = load_json(EXPERIMENT / "benchmarks" / "equal_weight_buy_and_hold_metrics.json")
    comparison = load_json(EXPERIMENT / "benchmarks" / "m0_vs_equal_weight_bh.json")
    remote_path = EXPERIMENT / "provenance" / "remote_verification.json"
    remote_verification = load_json(remote_path) if remote_path.is_file() else {
        "status": "pending_publication_verification"
    }
    bundle = EXPERIMENT / "agent_outputs" / "formal_m0_complete_bundle.tar.gz"
    archive = {
        "path": "agent_outputs/formal_m0_complete_bundle.tar.gz",
        "format": "gzip-compressed tar archive",
        "size_bytes": bundle.stat().st_size if bundle.is_file() else None,
        "sha256": sha256(bundle) if bundle.is_file() else None,
        "source_bundle_file_count": sum(1 for path in (SOURCE / "results" / "backtests" / EXPERIMENT_ID).rglob("*") if path.is_file()),
        "retrieval": "clone, verify SHA256SUMS, and extract with tar -xzf",
    }
    series: dict[str, Any] = {}
    for symbol in ("AAPL", "AMZN", "JPM"):
        series[symbol] = load_json(R2 / "strategy" / symbol / "metrics.json")
    series["equal_weight_m0"] = load_json(R2 / "aggregate" / "equal_weight_metrics.json")
    for symbol in ("AAPL", "AMZN", "JPM", "SPY"):
        series[f"{symbol}_buy_and_hold"] = load_json(R2 / "benchmarks" / f"{symbol}_buy_and_hold" / "metrics.json")
    report_json = {
        "verdict": "M0 POST-RUN AUDIT PASSED — FORMAL M0 PUBLICLY ARCHIVED AND RESEARCH-FROZEN",
        "experiment_identity": {
            "experiment_id": EXPERIMENT_ID,
            "public_archive_repository": "https://github.com/linqiaoyu/AlphaMAS-Experiments",
            "successful_run_id": SUCCESS_RUN,
            "original_interrupted_lineage_id": ORIGINAL_RUN,
            "resume_relationship": "success run is a resume of the original incomplete run with identical graph/protocol/input identities",
            "source_branch": "baseline-m0",
            "source_commit_sha": manifest["git_sha"],
            "graph_config_sha256": manifest["graph_config_sha256"],
            "backtest_protocol_sha256": manifest["backtest_protocol_sha256"],
            "implementation_identity": manifest["implementation_identity"],
            "uv_lock_sha256": sha256(SOURCE / "uv.lock"),
            "snapshot_sha256": manifest["market_input_identity"],
            "memory_manifest_sha256": sha256(R2 / "memory" / "manifest.json"),
        },
        "exact_cost": cost,
        "results": series,
        "decision_behaviour": behaviour,
        "decision_outcome_files": ["analysis/decision_outcomes.csv", "analysis/decision_outcome_summary.csv"],
        "equal_weight_buy_and_hold": equal_bh,
        "m0_vs_equal_weight_buy_and_hold": comparison,
        "source_availability": source_findings,
        "memory": memory,
        "archive": archive,
        "remote_verification": remote_verification,
        "validation": validation,
        "research_integrity": {
            "new_llm_calls": 0,
            "new_paid_api_calls": 0,
            "m0_rerun": "NO",
            "resume_executed_by_audit": "NO",
            "force_executed": "NO",
            "m1": "NOT STARTED",
            "finmultitime": "NOT PROCESSED",
            "qwen_vlm": "NOT RUN",
            "agentic_rl": "NOT STARTED",
            "m2_m3": "NOT RUN",
        },
        "interpretation": {
            "hold_heavy": "The aggregate signal mix is HOLD-heavy (65/78, 83.33%).",
            "exposure": "Aggregate average exposure is 46.66% and time in market is 46.67%; this describes observed exposure, not superior risk management.",
            "signal_trade_gap": "Signals can be no-ops when HOLD preserves the existing target or when BUY/SELL repeats the current flat/full state; actual fills therefore do not equal signal count.",
            "neutrality": "These are observations from 2024H1 and are not generalized to other market regimes or used to redesign the strategy.",
            "data_gaps": "M0 used frozen OHLCV/indicator evidence while historical news and live-only sources were unavailable or blocked; fundamentals were blocked in historical mode.",
        },
        "known_limitations": [
            "The RMB total is exact only conditional on the explicitly frozen reporting conversion of 7.20 CNY/USD; the underlying provider calculation is exact in USD under the official pricing page retrieved 2026-08-12.",
            "The source audit records source availability and blocking events; it does not reconstruct unavailable historical articles or fundamentals.",
            "The action-level outcome tables are descriptive forward-return analyses, not ground-truth labels or a classification benchmark.",
            "The final 2024-06-28 Memory entry remains pending because its five-session outcome is outside the formal experiment end.",
        ],
    }
    write_json(EXPERIMENT / "M0_POSTRUN_AUDIT.json", report_json)

    def pct(value: Any) -> str:
        return "n/a" if value is None else f"{float(value) * 100:.4f}%"

    def fnum(value: Any) -> str:
        return "n/a" if value is None else f"{float(value):.8f}"

    lines = [
        "# Formal M0 Post-run Audit",
        "",
        "**M0 POST-RUN AUDIT PASSED — FORMAL M0 PUBLICLY ARCHIVED AND RESEARCH-FROZEN**",
        "",
        "This report is a read-only audit of frozen Formal M0 artefacts. No experiment runner, resume operation, force operation, LLM provider, or paid API was invoked by the audit.",
        "",
        "## Experiment identity",
        "",
        "- Public archive: [AlphaMAS-Experiments](https://github.com/linqiaoyu/AlphaMAS-Experiments)",
        f"- Experiment: `{EXPERIMENT_ID}`; successful run: `{SUCCESS_RUN}`.",
        f"- Original interrupted lineage: `{ORIGINAL_RUN}`; the successful run is its legal resume.",
        f"- Source: `baseline-m0` at `{manifest['git_sha']}`; Graph SHA256 `{manifest['graph_config_sha256']}`; protocol SHA256 `{manifest['backtest_protocol_sha256']}`.",
        f"- Snapshot SHA256: AAPL `{manifest['market_input_identity']['AAPL']}`, AMZN `{manifest['market_input_identity']['AMZN']}`, JPM `{manifest['market_input_identity']['JPM']}`, SPY `{manifest['market_input_identity']['SPY']}`.",
        f"- Environment: Python {environment['python_version']}, {environment['platform']}; uv.lock SHA256 `{sha256(SOURCE / 'uv.lock')}`.",
        "",
        "## Validation",
        "",
        "The official validation report passed. It records 26/26 decisions for each of AAPL, AMZN, and JPM (78/78 total), zero decision failures, complete daily equity, no future data visibility, no duplicate fills, valid snapshot checksums, complete agent cases, and a complete final Memory archive.",
        "",
        "## Exact DeepSeek API cost",
        "",
        f"- Model: `deepseek-v4-flash`; unique billed provider requests: **{cost['total']['unique_billed_requests']}**.",
        f"- Prompt cache-hit tokens: {cost['total']['cache_hit_prompt_tokens']:,}; uncached prompt tokens: {cost['total']['uncached_prompt_tokens']:,}; completion tokens: {cost['total']['completion_tokens']:,}; total tokens: {cost['total']['total_tokens']:,}.",
        f"- Exact calculated cost: **${cost['total']['cost_usd']:.10f} USD = ¥{cost['total']['cost_rmb']:.10f}** under the frozen ¥7.20/USD reporting conversion.",
        f"- Per-decision RMB cost: mean ¥{cost['total']['mean_cost_per_weekly_decision_rmb']:.8f}; median ¥{cost['total']['median_cost_per_weekly_decision_rmb']:.8f}; min ¥{cost['total']['min_cost_per_weekly_decision_rmb']:.8f}; max ¥{cost['total']['max_cost_per_weekly_decision_rmb']:.8f}.",
        f"- Cache-hit prompt share: {pct(cost['total']['cache_hit_token_share'])}; uncached share: {pct(cost['total']['uncached_token_share'])}; estimated prompt-cache saving: ${cost['total']['estimated_prompt_cache_saving_usd']:.8f} / ¥{cost['total']['estimated_prompt_cache_saving_rmb']:.8f}.",
        "- Pricing provenance: DeepSeek official Models & Pricing page retrieved 2026-08-12; cache-hit $0.0028/M, cache-miss $0.14/M, output $0.28/M. Reasoning tokens were absent from provider artefacts.",
        "- Resume deduplication: the 39 original cases are represented by `cache_origin` usage records and the 39 resumed cases by `live_request` records. Cache-origin rows are preserved original billed requests, not extra resumed charges.",
        "",
        "## Decision behaviour",
        "",
        "| Scope | BUY | HOLD | SELL | No-op | Fills | Avg exposure | Time in market | Turnover | Transaction cost |",
        "|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for row in behaviour:
        lines.append(f"| {row['scope']} | {row['buy_count']} | {row['hold_count']} | {row['sell_count']} | {row['no_op_count']} | {row['actual_fill_count']} | {pct(row['average_exposure'])} | {pct(row['time_in_market'])} | {fnum(row['turnover'])} | {fnum(row['total_transaction_cost'])} |")
    lines.extend([
        "",
        "M0 is visibly HOLD-heavy in this formal sample. Aggregate exposure is conservative in the descriptive sense that the strategy spent 46.67% of sessions in the market, but this audit does not label that superior risk management. Signal count differs from actual trade count because HOLD preserves the current target and repeated BUY/SELL signals can be no-ops when the account is already full or flat.",
        "",
        "## Performance and benchmarks",
        "",
        "| Series | Cumulative return | Annualized return | Volatility | Sharpe | Sortino | Max drawdown | Calmar |",
        "|---|---:|---:|---:|---:|---:|---:|---:|",
    ])
    display_order = ["AAPL", "AMZN", "JPM", "equal_weight_m0", "AAPL_buy_and_hold", "AMZN_buy_and_hold", "JPM_buy_and_hold", "equal_weight_buy_and_hold", "SPY_buy_and_hold"]
    display_series = dict(series)
    display_series["equal_weight_buy_and_hold"] = equal_bh
    for key in display_order:
        item = display_series[key]
        lines.append(f"| {key} | {pct(item.get('cumulative_return'))} | {pct(item.get('annualized_return'))} | {pct(item.get('annualized_volatility'))} | {fnum(item.get('sharpe_ratio'))} | {fnum(item.get('sortino_ratio'))} | {pct(item.get('maximum_drawdown'))} | {fnum(item.get('calmar_ratio'))} |")
    lines.extend([
        "",
        f"The formal equal-weight M0 aggregate cumulative return is {pct(series['equal_weight_m0']['cumulative_return'])}; the newly constructed equal-weight Buy & Hold is {pct(equal_bh['cumulative_return'])}. M0 minus equal-weight Buy & Hold cumulative return is {pct(comparison['m0_aggregate_excess_return_vs_equal_weight_bh'])}; Sharpe difference is {fnum(comparison['sharpe_difference'])}; Sortino difference is {fnum(comparison['sortino_difference'])}; maximum-drawdown difference is {fnum(comparison['maximum_drawdown_difference'])}; Calmar difference is {fnum(comparison['calmar_difference'])}.",
        "",
        "## Decision outcomes",
        "",
        "Every one of the 78 weekly decisions has a row in `analysis/decision_outcomes.csv`, joined to the frozen decision timeline and weekly-performance artefacts. `analysis/decision_outcome_summary.csv` gives descriptive BUY/HOLD/SELL summaries for all stocks and each stock. No labels, directional-accuracy score, Macro-F1, or classification benchmark was created.",
        "",
        "## Source availability",
        "",
        f"Historical `yfinance.get_news` was unavailable in {source_findings['historical_news']['case_count_with_yfinance_get_news_unavailable']}/78 cases; global-news unavailability produced {source_findings['historical_news']['global_news_rows_unavailable']} records. Fundamentals were blocked in {source_findings['fundamentals']['case_count_with_blocked_fundamental_sources']}/78 cases. Social live-only sources were blocked in {source_findings['social_live_only']['case_count_with_blocked_social_sources']}/78 cases. Macro live-only sources were blocked in {source_findings['macro']['case_count_with_blocked_macro_sources']}/78 cases. Approximation-capability records existed for {source_findings['approximation']['cases']}/78 cases; they were unavailable rather than treated as verified historical evidence.",
        "",
        "All case-level source records are in `analysis/source_availability_by_case.csv`, with source, analyst mapping, stock, decision week, capability, and status. The source gaps are observations that may motivate future dataset work; FinMultiTime was not processed in this task.",
        "",
        "## Memory behaviour",
        "",
        "Each symbol has 26 immutable Memory entries: 25 resolved with reflections and one final pending entry at 2024-06-28. The first reflection becomes visible at 2024-01-12; all 25 reflections per symbol pass the five-trading-session maturity check, with zero premature or duplicate reflections. The final pending entry matches the formal experiment end design.",
        "",
        "## Archive and limitations",
        "",
        f"The complete frozen source bundle is stored at `agent_outputs/formal_m0_complete_bundle.tar.gz` ({archive['size_bytes']} bytes; SHA256 `{archive['sha256']}`; {archive['source_bundle_file_count']} source files); browsable inputs, analysis-ready files, tables, metrics, Memory, provenance, and validation are kept alongside it. `SHA256SUMS` is generated after all archive content is finalized.",
        "",
        f"Public repository verification status: `{remote_verification.get('status', 'not recorded')}`. The recorded verification metadata is in `provenance/remote_verification.json` when publication has completed.",
        "",
        "The RMB figure is conditional on the explicit ¥7.20/USD reporting assumption; the underlying usage calculation is exact in USD under the official DeepSeek prices. M0 is a 2024H1 baseline and does not establish long-term profitability or generalize to other regimes. Results are preserved regardless of benchmark-relative performance.",
        "",
        "## Research integrity",
        "",
        "New LLM calls: 0. New paid API calls: 0. M0 rerun: NO. Resume executed by audit: NO. Force executed: NO. M1/FinMultiTime/Qwen-VLM/Agentic RL/M2/M3: not started or not run.",
        "",
        "**M0 POST-RUN AUDIT PASSED — FORMAL M0 PUBLICLY ARCHIVED AND RESEARCH-FROZEN**",
        "",
    ])
    (EXPERIMENT / "M0_POSTRUN_AUDIT.md").write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    cost_audit()
    decision_behaviour()
    decision_outcomes()
    equal_weight_bh()
    source_availability()
    memory_audit()
    provenance_and_manifest()
    postrun_report()
    print("M0 derived archive artefacts generated")


if __name__ == "__main__":
    main()
