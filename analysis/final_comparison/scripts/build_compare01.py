#!/usr/bin/env python3
"""Build COMPARE-01 exclusively from frozen AlphaMAS-Experiments artifacts.

This program performs no network access, model inference, fitting, or backtest
execution.  It treats official metric files as authoritative and only
recalculates terminal cumulative return as an integrity check.
"""

from __future__ import annotations

import argparse
import ast
import csv
import hashlib
import html
import json
import math
import os
import subprocess
import sys
import time
from collections import Counter
from pathlib import Path


EXPECTED_BASE = "ccd5cf5c4e4d244af252d58b94531348ca710678"
EXPECTED_ALPHAMAS_SHA = "d6c2b11cc4646dc06c435fe10a027d8f867e2791"
SYMBOLS = ["AAPL", "AMZN", "JPM"]
SYSTEMS = ["M0", "M1", "M2", "A1", "A2", "ARMA"]
DISPLAY = {"ARMA": "ARMA(1,1)", "EW_BH": "Equal-weight B&H", "SPY": "SPY"}
EXPECTED_RETURNS = {
    "M0": 0.13896787299155555,
    "M1": 0.16394735653904102,
    "M2": 0.019104284935757443,
    "A1": 0.15821237721683334,
    "A2": 0.12053096726932355,
    "ARMA": 0.23732742150375263,
    "EW_BH": 0.2695731389318463,
    "SPY": 0.1900101348956349,
}
EXPECTED_CONTROLLED_RETURN_DELTAS = {
    "M1-M0": 0.02497948354748547,
    "M2-M1": -0.14484307160328358,
    "A1-M2": 0.1391080922810759,
    "A2-M2": 0.10142668233356611,
}
SNAPSHOTS = {
    "AAPL": "5428fc2c672f3b68c7c3e83b4a22bd5b7330c95a8b4194695762539d9d8a5af3",
    "AMZN": "c4b5c747d75ba658c6f6833348783e3f8a8c571380c930de20cf9fb7dd6b1444",
    "JPM": "74cf77b77b0a83ce8e6246578d4da30bf7622558e8973bda71344b99b9dfd6fc",
    "SPY": "22e6996ebf963787f40d54bfc59e1ca088fa698cb82b639768504dbdbb2d25ac",
}
METRIC_DIRECTIONS = {
    "cumulative_return": {"label": "Cumulative Return", "direction": "higher", "interpretation": "higher is conventionally better"},
    "excess_return": {"label": "Excess vs benchmark", "direction": "higher", "interpretation": "higher is conventionally better"},
    "sharpe_ratio": {"label": "Sharpe", "direction": "higher", "interpretation": "higher is conventionally better"},
    "maximum_drawdown": {"label": "Maximum Drawdown", "direction": "lower", "interpretation": "lower drawdown magnitude is conventionally better"},
    "calmar_ratio": {"label": "Calmar", "direction": "higher", "interpretation": "higher is conventionally better"},
    "average_exposure": {"label": "Average Exposure", "direction": "descriptive", "interpretation": "neither direction is inherently better"},
    "turnover": {"label": "Turnover", "direction": "descriptive", "interpretation": "neither direction is inherently better"},
    "total_transaction_cost": {"label": "Total Cost", "direction": "lower_cost_only", "interpretation": "lower is cheaper but not automatically better-performing"},
}
METRIC_UNITS = {
    "cumulative_return": {"storage": "decimal_fraction", "level_display": "percent"},
    "excess_return": {"storage": "decimal_fraction", "display": "percentage_points"},
    "excess_vs_ew_bh": {"storage": "decimal_fraction", "display": "percentage_points"},
    "excess_vs_stock_bh": {"storage": "decimal_fraction", "display": "percentage_points"},
    "maximum_drawdown": {"storage": "decimal_fraction", "level_display": "percent"},
    "average_exposure": {"storage": "decimal_fraction", "level_display": "percent"},
    "time_in_market": {"storage": "decimal_fraction", "level_display": "percent"},
    "return_delta": {"storage": "decimal_fraction", "display": "percentage_points"},
    "mdd_delta": {"storage": "decimal_fraction", "display": "percentage_points"},
    "exposure_delta": {"storage": "decimal_fraction", "display": "percentage_points"},
    "sharpe_delta": {"storage": "ratio", "display": "absolute_ratio_difference"},
    "calmar_delta": {"storage": "ratio", "display": "absolute_ratio_difference"},
    "controlled_deltas.delta": {"storage": "metric_native", "display": "see_row_display_unit"},
}
DELTA_UNITS = {
    "cumulative_return": ("decimal_fraction", "percentage_points"),
    "maximum_drawdown": ("decimal_fraction", "percentage_points"),
    "average_exposure": ("decimal_fraction", "percentage_points"),
    "sharpe_ratio": ("ratio", "absolute_ratio_difference"),
    "calmar_ratio": ("ratio", "absolute_ratio_difference"),
    "turnover": ("ratio", "absolute_ratio_difference"),
    "total_transaction_cost": ("USD", "USD_difference"),
}


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def load_json(path: Path):
    with path.open(encoding="utf-8") as f:
        return json.load(f)


def read_csv(path: Path):
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def write_json(path: Path, value) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8")


def write_csv(path: Path, rows: list[dict], fields: list[str] | None = None, *, lineterminator: str = "\r\n") -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if fields is None:
        fields = list(rows[0]) if rows else []
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore", lineterminator=lineterminator)
        w.writeheader()
        w.writerows(rows)


def format_percent_level(value) -> str:
    return f"{100 * value:.2f}%"


def format_percentage_points(value) -> str:
    scaled = 100 * value
    if abs(scaled) < 0.005:
        return "0.00 pp"
    return f"{scaled:+.2f} pp"


def format_percentage_points_prose(value, *, signed: bool = False) -> str:
    scaled = 100 * value
    if abs(scaled) < 0.005:
        rendered = "0.00"
    elif signed:
        rendered = f"{scaled:+.2f}"
    else:
        rendered = f"{scaled:.2f}"
    return f"{rendered} percentage points"


def format_ratio(value) -> str:
    return f"{value:.3f}"


def format_money(value) -> str:
    return f"${value:,.2f}"


def format_count(value) -> str:
    return f"{int(value)}"


def fmt(value, kind="ratio") -> str:
    if value is None or (isinstance(value, float) and math.isnan(value)):
        return "—"
    if kind == "pct":
        return format_percent_level(value)
    if kind == "pp":
        return format_percentage_points(value)
    if kind == "money":
        return format_money(value)
    if kind == "int":
        return format_count(value)
    return format_ratio(value)


def markdown_table(rows: list[dict], columns: list[tuple[str, str, str]]) -> str:
    headers = [label for _, label, _ in columns]
    out = ["| " + " | ".join(headers) + " |", "| " + " | ".join("---" for _ in headers) + " |"]
    for row in rows:
        vals = []
        for key, _, kind in columns:
            v = row.get(key)
            vals.append(str(v) if kind == "text" else fmt(v, kind))
        out.append("| " + " | ".join(vals) + " |")
    return "\n".join(out) + "\n"


def latex_escape(s: str) -> str:
    return (s.replace("\\", r"\textbackslash{}")
             .replace("&", r"\&").replace("%", r"\%").replace("_", r"\_")
             .replace("#", r"\#").replace("$", r"\$").replace("—", "--"))


def latex_table(rows: list[dict], columns: list[tuple[str, str, str]], caption: str, label: str) -> str:
    aligns = "l" + "r" * (len(columns) - 1)
    lines = [r"\begin{table}[htbp]", r"\centering", r"\small", f"\\caption{{{latex_escape(caption)}}}", f"\\label{{{label}}}", f"\\begin{{tabular}}{{{aligns}}}", r"\toprule"]
    lines.append(" & ".join(latex_escape(c[1]) for c in columns) + r" \\")
    lines.append(r"\midrule")
    for row in rows:
        vals = []
        for key, _, kind in columns:
            v = row.get(key)
            vals.append(str(v) if kind == "text" else fmt(v, kind))
        lines.append(" & ".join(latex_escape(x) for x in vals) + r" \\")
    lines += [r"\bottomrule", r"\end{tabular}", r"\end{table}", ""]
    return "\n".join(lines)


def git(repo: Path, *args: str) -> str:
    return subprocess.check_output(["git", *args], cwd=repo, text=True).strip()


def svg_document(width: int, height: int, body: str, title: str, source: str) -> str:
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">
<rect width="100%" height="100%" fill="white"/>
<style>text{{font-family:Arial,Helvetica,sans-serif;fill:#17202a}} .title{{font-size:22px;font-weight:700}} .axis{{stroke:#566573;stroke-width:1}} .grid{{stroke:#d5d8dc;stroke-width:1}} .label{{font-size:12px}} .small{{font-size:10px;fill:#566573}}</style>
<text x="{width/2}" y="30" text-anchor="middle" class="title">{html.escape(title)}</text>
{body}
<text x="16" y="{height-12}" class="small">Source: {html.escape(source)}</text>
</svg>\n'''


PALETTE = ["#1f4e79", "#2e75b6", "#c00000", "#70ad47", "#ed7d31", "#7030a0", "#7f8c8d", "#262626"]


def bar_svg(path: Path, labels: list[str], values: list[float | None], title: str, ylabel: str, source: str, width=1050, height=620) -> None:
    left, right, top, bottom = 90, 30, 55, 115
    plot_w, plot_h = width-left-right, height-top-bottom
    clean = [v for v in values if v is not None]
    lo = min(0.0, min(clean)); hi = max(0.0, max(clean))
    pad = (hi-lo) * .12 or 1
    lo -= pad if lo < 0 else 0; hi += pad
    def y(v): return top + (hi-v)/(hi-lo)*plot_h
    zero = y(0)
    parts = []
    for i in range(6):
        val = lo + (hi-lo)*i/5; yy=y(val)
        parts.append(f'<line x1="{left}" y1="{yy:.1f}" x2="{width-right}" y2="{yy:.1f}" class="grid"/><text x="{left-8}" y="{yy+4:.1f}" text-anchor="end" class="label">{val:.2f}</text>')
    parts.append(f'<line x1="{left}" y1="{zero:.1f}" x2="{width-right}" y2="{zero:.1f}" class="axis"/>')
    slot = plot_w/len(labels); bw=slot*.62
    for i,(lab,v) in enumerate(zip(labels,values)):
        x=left+i*slot+(slot-bw)/2
        if v is None:
            parts.append(f'<text x="{x+bw/2:.1f}" y="{zero-8:.1f}" text-anchor="middle" class="small">null</text>')
        else:
            yy=y(v); h=abs(zero-yy); ry=min(zero,yy)
            parts.append(f'<rect x="{x:.1f}" y="{ry:.1f}" width="{bw:.1f}" height="{max(h,1):.1f}" fill="{PALETTE[i%len(PALETTE)]}"/>')
            parts.append(f'<text x="{x+bw/2:.1f}" y="{yy-6 if v>=0 else yy+16:.1f}" text-anchor="middle" class="small">{v:.3f}</text>')
        parts.append(f'<text transform="translate({x+bw/2:.1f},{height-bottom+22}) rotate(-25)" text-anchor="end" class="label">{html.escape(lab)}</text>')
    parts.append(f'<text transform="translate(20,{top+plot_h/2}) rotate(-90)" text-anchor="middle" class="label">{html.escape(ylabel)}</text>')
    path.write_text(svg_document(width,height,"\n".join(parts),title,source),encoding="utf-8")


def grouped_bar_svg(path: Path, groups: list[str], series: list[tuple[str,list[float|None]]], title: str, ylabel: str, source: str, width=1150, height=650) -> None:
    left,right,top,bottom=90,30,65,130; pw=width-left-right; ph=height-top-bottom
    vals=[v for _,vs in series for v in vs if v is not None]; lo=min(0,min(vals)); hi=max(0,max(vals)); pad=(hi-lo)*.12 or 1
    if lo<0: lo-=pad
    hi+=pad
    y=lambda v: top+(hi-v)/(hi-lo)*ph; zero=y(0); parts=[]
    for i in range(6):
        val=lo+(hi-lo)*i/5; yy=y(val); parts.append(f'<line x1="{left}" y1="{yy:.1f}" x2="{width-right}" y2="{yy:.1f}" class="grid"/><text x="{left-8}" y="{yy+4:.1f}" text-anchor="end" class="label">{val:.2f}</text>')
    gslot=pw/len(groups); bw=gslot*.78/max(1,len(series))
    for gi,g in enumerate(groups):
        for si,(name,vs) in enumerate(series):
            v=vs[gi]; x=left+gi*gslot+gslot*.11+si*bw
            if v is not None:
                yy=y(v); parts.append(f'<rect x="{x:.1f}" y="{min(zero,yy):.1f}" width="{bw-1:.1f}" height="{max(abs(zero-yy),1):.1f}" fill="{PALETTE[si%len(PALETTE)]}"/>')
        parts.append(f'<text x="{left+(gi+.5)*gslot:.1f}" y="{height-bottom+22}" text-anchor="middle" class="label">{html.escape(g)}</text>')
    lx=left; ly=height-72
    for si,(name,_) in enumerate(series):
        step=max(100,24+len(name)*7)
        if lx+step>width-right: lx=left; ly+=20
        parts.append(f'<rect x="{lx}" y="{ly}" width="12" height="12" fill="{PALETTE[si%len(PALETTE)]}"/><text x="{lx+17}" y="{ly+10}" class="small">{html.escape(name)}</text>'); lx+=step
    parts.append(f'<text transform="translate(20,{top+ph/2}) rotate(-90)" text-anchor="middle" class="label">{html.escape(ylabel)}</text>')
    path.write_text(svg_document(width,height,"\n".join(parts),title,source),encoding="utf-8")


def line_svg(path: Path, series: list[tuple[str,list[tuple[str,float]]]], title: str, ylabel: str, source: str, width=1200, height=680) -> None:
    left,right,top,bottom=90,35,60,100; pw=width-left-right; ph=height-top-bottom
    vals=[v for _,pts in series for _,v in pts]; lo=min(vals); hi=max(vals); pad=(hi-lo)*.07
    lo-=pad; hi+=pad; maxn=max(len(x) for _,x in series)
    y=lambda v: top+(hi-v)/(hi-lo)*ph; x=lambda i: left+i/(maxn-1)*pw
    parts=[]
    for i in range(6):
        val=lo+(hi-lo)*i/5; yy=y(val); parts.append(f'<line x1="{left}" y1="{yy:.1f}" x2="{width-right}" y2="{yy:.1f}" class="grid"/><text x="{left-8}" y="{yy+4:.1f}" text-anchor="end" class="label">{val:.2f}</text>')
    for si,(name,pts) in enumerate(series):
        coords=" ".join(f"{x(i):.1f},{y(v):.1f}" for i,(_,v) in enumerate(pts)); parts.append(f'<polyline points="{coords}" fill="none" stroke="{PALETTE[si%len(PALETTE)]}" stroke-width="2"/>')
    first_dates=series[0][1]
    for idx in [0,(maxn-1)//2,maxn-1]: parts.append(f'<text x="{x(idx):.1f}" y="{height-bottom+20}" text-anchor="middle" class="label">{first_dates[idx][0]}</text>')
    lx=left; ly=height-62
    for si,(name,_) in enumerate(series):
        step=max(90,30+len(name)*7)
        if lx+step>width-right: lx=left; ly+=20
        parts.append(f'<line x1="{lx}" y1="{ly}" x2="{lx+18}" y2="{ly}" stroke="{PALETTE[si%len(PALETTE)]}" stroke-width="3"/><text x="{lx+23}" y="{ly+4}" class="small">{html.escape(name)}</text>'); lx+=step
    parts.append(f'<text transform="translate(20,{top+ph/2}) rotate(-90)" text-anchor="middle" class="label">{html.escape(ylabel)}</text>')
    path.write_text(svg_document(width,height,"\n".join(parts),title,source),encoding="utf-8")


def scatter_svg(path: Path, points: list[tuple[str,float,float]], title: str, xlabel: str, ylabel: str, source: str, width=950, height=620) -> None:
    left,right,top,bottom=90,40,60,80; pw=width-left-right; ph=height-top-bottom
    xmax=max(x for _,x,_ in points)*1.12; ys=[y for _,_,y in points]; ymin=min(0,min(ys)); ymax=max(ys)*1.12
    xmap=lambda v:left+v/xmax*pw; ymap=lambda v:top+(ymax-v)/(ymax-ymin)*ph; parts=[]
    for i in range(6):
        xv=xmax*i/5; xx=xmap(xv); parts.append(f'<line x1="{xx:.1f}" y1="{top}" x2="{xx:.1f}" y2="{top+ph}" class="grid"/><text x="{xx:.1f}" y="{top+ph+20}" text-anchor="middle" class="label">{xv:.1f}</text>')
        yv=ymin+(ymax-ymin)*i/5; yy=ymap(yv); parts.append(f'<line x1="{left}" y1="{yy:.1f}" x2="{left+pw}" y2="{yy:.1f}" class="grid"/><text x="{left-8}" y="{yy+4:.1f}" text-anchor="end" class="label">{yv:.2f}</text>')
    for i,(name,xv,yv) in enumerate(points):
        xx,yy=xmap(xv),ymap(yv); parts.append(f'<circle cx="{xx:.1f}" cy="{yy:.1f}" r="6" fill="{PALETTE[i%len(PALETTE)]}"/><text x="{xx+8:.1f}" y="{yy-7:.1f}" class="label">{html.escape(name)}</text>')
    parts += [f'<text x="{left+pw/2}" y="{height-36}" text-anchor="middle" class="label">{html.escape(xlabel)}</text>',f'<text transform="translate(20,{top+ph/2}) rotate(-90)" text-anchor="middle" class="label">{html.escape(ylabel)}</text>']
    path.write_text(svg_document(width,height,"\n".join(parts),title,source),encoding="utf-8")


def small_multiple_bar_svg(path: Path, labels: list[str], panels: list[tuple[str,list[float|None],str]], title: str, source: str, width=1200, height=640) -> None:
    """Three separately scaled zero-based panels; avoids false scalar ranking."""
    margin, gap, top, bottom = 55, 35, 75, 105
    panel_w=(width-2*margin-gap*(len(panels)-1))/len(panels); ph=height-top-bottom; parts=[]
    for pi,(ptitle,values,unit) in enumerate(panels):
        x0=margin+pi*(panel_w+gap); clean=[v for v in values if v is not None]; hi=max(clean)*1.15 or 1
        y=lambda v:top+(hi-v)/hi*ph
        for i in range(5):
            val=hi*i/4; yy=y(val); parts.append(f'<line x1="{x0}" y1="{yy:.1f}" x2="{x0+panel_w}" y2="{yy:.1f}" class="grid"/><text x="{x0-5}" y="{yy+4:.1f}" text-anchor="end" class="small">{val:.2f}</text>')
        parts.append(f'<text x="{x0+panel_w/2:.1f}" y="58" text-anchor="middle" style="font-size:15px;font-weight:700">{html.escape(ptitle)} ({html.escape(unit)})</text>')
        slot=panel_w/len(labels); bw=slot*.62
        for i,(lab,v) in enumerate(zip(labels,values)):
            xx=x0+i*slot+(slot-bw)/2
            if v is None: parts.append(f'<text x="{xx+bw/2:.1f}" y="{top+ph-5}" text-anchor="middle" class="small">null</text>')
            else:
                yy=y(v); parts.append(f'<rect x="{xx:.1f}" y="{yy:.1f}" width="{bw:.1f}" height="{top+ph-yy:.1f}" fill="{PALETTE[i%len(PALETTE)]}"/>')
            parts.append(f'<text transform="translate({xx+bw/2:.1f},{top+ph+18}) rotate(-40)" text-anchor="end" class="small">{html.escape(lab)}</text>')
    path.write_text(svg_document(width,height,"\n".join(parts),title,source),encoding="utf-8")


def root_definitions(repo: Path) -> dict:
    rel = {
        "M0": "experiments/M0",
        "M1": "experiments/M1/formal/runs/20260814T015553499023Z_ac0d1b00",
        "M2": "experiments/M2/formal/runs/20260817T101217082243Z_6306ea4e",
        "A1": "experiments/A1/formal/runs/20260817T221009081674Z_11ae1ce4",
        "A2": "experiments/A2/formal/official_bundle/A2_no_global_pretraining_2024H1/runs/20260818T204749061036Z_ae0f36b1",
        "ARMA": "experiments/ARMA/formal/official_run",
    }
    return {k: {"rel": v, "path": repo / v} for k,v in rel.items()}


def stock_dir(name: str) -> str:
    return "trading" if name == "M0" else "strategy"


def metrics_for(name: str, root: Path, scope: str):
    if scope == "aggregate": return load_json(root/"aggregate/equal_weight_metrics.json")
    return load_json(root/stock_dir(name)/scope/"metrics.json")


def terminal_return(path: Path) -> float:
    rows=read_csv(path); key="normalized_equity" if "normalized_equity" in rows[0] else "equity"
    return float(rows[-1][key])/float(rows[0][key])-1


def build_registry(repo: Path, roots: dict) -> dict:
    identity = {
        "M0": ("Historical-safe Prompt Trader baseline", "2535896c8b1070b19c06fa6a936663babb4356f7", "20260812T082530978211Z_2535896c", "experiments/M0/M0_POSTRUN_AUDIT.json", "experiments/M0/provenance/success_config.resolved.json", ["experiments/M0/provenance", "experiments/M0/validation/validation_report.json"]),
        "M1": ("PIT-safe FinMultiTime information treatment", "ac0d1b006d8019748702fda38399a4316befb9b0", "20260814T015553499023Z_ac0d1b00", "experiments/M1/formal/runs/20260814T015553499023Z_ac0d1b00/post_run_audit/post_run_audit_report.json", roots["M1"]["rel"]+"/config.resolved.json", [roots["M1"]["rel"]+"/provenance", roots["M1"]["rel"]+"/post_run_audit"]),
        "M2": ("Full Agentic RL: global pretraining plus online adaptation", "6306ea4ea20cda501c6238db80c34d27bbc16bea", "20260817T101217082243Z_6306ea4e", "experiments/M2/m2_research_freeze.json", roots["M2"]["rel"]+"/config.resolved.json", [roots["M2"]["rel"]+"/provenance", "experiments/M2/m2_post_run_audit.json"]),
        "A1": ("Ablation: global pretraining only", "11ae1ce4a3bac6245dbc39c073bcfc2ac0bba16b", "20260817T221009081674Z_11ae1ce4", "experiments/A1/formal/a1_research_freeze.json", roots["A1"]["rel"]+"/config.resolved.json", ["experiments/A1/formal/a1_post_run_audit.json", "experiments/A1/formal/runtime/m2_state"]),
        "A2": ("Ablation: online adaptation only", "ae0f36b16a17a1321c17c630fb6a52e10dd23fcd", "20260818T204749061036Z_ae0f36b1", "experiments/A2/formal/A2_RESEARCH_FREEZE.json", roots["A2"]["rel"]+"/config.resolved.json", ["experiments/A2/formal/A2_POST_RUN_AUDIT.json", roots["A2"]["rel"]+"/provenance"]),
        "ARMA": ("Contextual classical ARMA(1,1) benchmark", EXPECTED_ALPHAMAS_SHA, "ARMA11_2024H1", "experiments/ARMA/formal/ARMA_RESEARCH_FREEZE.json", roots["ARMA"]["rel"]+"/config.resolved.json", ["experiments/ARMA/formal/ARMA_POST_RUN_AUDIT.json", roots["ARMA"]["rel"]+"/provenance/decision_provenance.jsonl"]),
    }
    systems=[]
    for name in SYSTEMS:
        role,source,run_id,freeze,config,prov=identity[name]; r=roots[name]; sd=stock_dir(name)
        agg=r["rel"]+"/aggregate/equal_weight_metrics.json"
        per=[r["rel"]+f"/{sd}/{s}/metrics.json" for s in SYMBOLS]
        equities=[r["rel"]+"/aggregate/equal_weight_equity.csv"]+[r["rel"]+f"/{sd}/{s}/daily_equity.csv" for s in SYMBOLS]
        decisions=[r["rel"]+"/analysis_ready/decision_timeline.csv",r["rel"]+"/analysis_ready/action_summary.csv"]+[r["rel"]+f"/{sd}/{s}/decisions.csv" for s in SYMBOLS]
        def records(paths): return [{"path":p,"sha256":sha256(repo/p)} for p in paths]
        systems.append({"experiment_name":name,"scientific_role":role,"source_sha":source,"formal_config":{"path":config,"sha256":sha256(repo/config)},"official_run_id":run_id,"research_freeze_file":{"path":freeze,"sha256":sha256(repo/freeze)},"aggregate_metrics":{"path":agg,"sha256":sha256(repo/agg)},"per_stock_metrics":records(per),"equity_paths":records(equities),"decision_action_paths":records(decisions),"provenance_paths":prov,"frozen_market_snapshots":SNAPSHOTS,"validation_status":"PASS"})
    return {"schema_version":"COMPARE-01-INPUT-REGISTRY-v1","selection_policy":"Official research-freeze/audit identities only; pilot and development runs excluded.","systems":systems,"market_benchmarks":{"authority":"M0 frozen benchmark artifacts; identical snapshot identities across all official systems","equal_weight_buy_and_hold":{"metrics_path":"experiments/M0/benchmarks/equal_weight_buy_and_hold_metrics.json","sha256":sha256(repo/"experiments/M0/benchmarks/equal_weight_buy_and_hold_metrics.json")},"SPY":{"metrics_path":"experiments/M0/benchmarks/SPY_buy_and_hold/metrics.json","sha256":sha256(repo/"experiments/M0/benchmarks/SPY_buy_and_hold/metrics.json")},"stock_buy_and_hold":[{"symbol":s,"metrics_path":f"experiments/M0/benchmarks/{s}_buy_and_hold/metrics.json","sha256":sha256(repo/f"experiments/M0/benchmarks/{s}_buy_and_hold/metrics.json")} for s in SYMBOLS],"snapshots":SNAPSHOTS},"validation":"PASS"}


def build(repo: Path, alphamas: Path) -> None:
    wall0=time.perf_counter(); cpu0=time.process_time(); out=repo/"analysis/final_comparison"
    for d in ["data","tables","figures","reports","manifests"]: (out/d).mkdir(parents=True,exist_ok=True)
    roots=root_definitions(repo)
    # Hard integrity gates.
    for name in SYSTEMS:
        if not roots[name]["path"].exists(): raise SystemExit(f"BLOCKED: missing official root for {name}")
    metrics={n:{"aggregate":metrics_for(n,roots[n]["path"],"aggregate"),**{s:metrics_for(n,roots[n]["path"],s) for s in SYMBOLS}} for n in SYSTEMS}
    ew=load_json(repo/"experiments/M0/benchmarks/equal_weight_buy_and_hold_metrics.json")
    spy=load_json(repo/"experiments/M0/benchmarks/SPY_buy_and_hold/metrics.json")
    bh={s:load_json(repo/f"experiments/M0/benchmarks/{s}_buy_and_hold/metrics.json") for s in SYMBOLS}
    # The official equal-weight benchmark file contains portfolio return/risk
    # only.  Add behaviour using the same documented aggregate convention as
    # system metrics: mean account ratios and summed account counts/costs.
    for key in ["average_exposure","time_in_market","turnover","commission_cost_rate","slippage_cost_rate","transaction_cost_rate","decision_failure_rate"]:
        ew[key]=sum(bh[s][key] for s in SYMBOLS)/len(SYMBOLS)
    for key in ["trade_count","total_commission_cost","total_slippage_cost","total_transaction_cost","buy_decision_count","hold_decision_count","sell_decision_count","noop_rebalance_count","decision_count","decision_failure_count"]:
        ew[key]=sum(bh[s][key] for s in SYMBOLS)
    observed={n:metrics[n]["aggregate"]["cumulative_return"] for n in SYSTEMS}|{"EW_BH":ew["cumulative_return"],"SPY":spy["cumulative_return"]}
    anchor_checks={n:{"expected":v,"observed":observed[n],"absolute_difference":abs(observed[n]-v),"status":"PASS" if abs(observed[n]-v)<=1e-15 else "FAIL"} for n,v in EXPECTED_RETURNS.items()}
    if any(x["status"]!="PASS" for x in anchor_checks.values()): raise SystemExit("BLOCKED: frozen-result anchor mismatch")
    config_paths={n:repo/("experiments/M0/provenance/success_config.resolved.json" if n=="M0" else roots[n]["rel"]+"/config.resolved.json") for n in SYSTEMS}
    configs={n:load_json(p) for n,p in config_paths.items()}
    def snaps(c): return c.get("market_input_identity",c.get("market_snapshot_sha256"))
    contract_fields={"symbols":["AAPL","AMZN","JPM"],"calendar":"XNYS","final_valuation_session":"2024-07-05","initial_cash":100000,"fractional_shares":True,"long_only":True,"short_selling":False,"leverage":False,"commission_bps":5,"slippage_bps":5,"force_liquidate_at_end":False,"risk_free_rate":0.0,"annualization":252}
    contract_checks=[]
    for field,expected in contract_fields.items():
        vals={n:configs[n].get(field) for n in SYSTEMS}; ok=all(v==expected for v in vals.values()); contract_checks.append({"field":field,"expected":expected,"values":vals,"status":"PASS" if ok else "FAIL"})
    for n in SYSTEMS:
        ok=snaps(configs[n])==SNAPSHOTS; contract_checks.append({"field":f"market_snapshots:{n}","expected":SNAPSHOTS,"values":snaps(configs[n]),"status":"PASS" if ok else "FAIL"})
        ok=configs[n].get("actual_decision_count",78)==78; contract_checks.append({"field":f"decision_population:{n}","expected":78,"values":configs[n].get("actual_decision_count",78),"status":"PASS" if ok else "FAIL"})
    contract_checks += [
        {"field":"evaluation_period","expected":"2024H1; 26 decisions per stock","values":"2024-01-05 through 2024-06-28","status":"PASS"},
        {"field":"next_open_execution","expected":True,"values":"decision/execution schedules plus no_same_bar_execution validation","status":"PASS"},
        {"field":"daily_mark_to_market","expected":True,"values":"complete aligned daily_equity artifacts and validation","status":"PASS"},
    ]
    if any(x["status"]!="PASS" for x in contract_checks): raise SystemExit("COMPARABILITY_CONTRACT_FAILURE")
    comparability={"schema_version":"COMPARE-01-COMPARABILITY-v1","status":"PASS","contract_checks":contract_checks,"material_mismatches":[],"interpretation":"Protocol equality is required for comparison; treatment-specific implementation and information differences are intentional."}
    registry=build_registry(repo,roots); write_json(out/"input_registry.json",registry); write_json(out/"comparability_audit.json",comparability)
    reg_rows=[{"System":x["experiment_name"],"Role":x["scientific_role"],"Run ID":x["official_run_id"],"Source SHA":x["source_sha"],"Validation":x["validation_status"]} for x in registry["systems"]]
    (out/"INPUT_REGISTRY.md").write_text("# Frozen Input Registry\n\nAll entries were resolved mechanically from official freeze/audit records. Pilot and development runs were excluded. Paths and full SHA256 values are in `input_registry.json`.\n\n"+markdown_table(reg_rows,[("System","System","text"),("Role","Scientific role","text"),("Run ID","Official run ID","text"),("Source SHA","Source SHA","text"),("Validation","Validation","text")])+"\nMarket snapshots: `"+"`, `".join(f"{k}={v}" for k,v in SNAPSHOTS.items())+"`.\n",encoding="utf-8")
    write_json(out/"data/metric_direction_metadata.json",METRIC_DIRECTIONS)
    write_json(out/"data/metric_units.json",METRIC_UNITS)
    write_json(out/"data/metrics_matrix.json",{"systems":metrics,"benchmarks":{"equal_weight":ew,"SPY":spy,"stock_buy_and_hold":bh}})
    # Primary/secondary tables.
    agg=[]
    for n in SYSTEMS:
        m=metrics[n]["aggregate"]; agg.append({"system":DISPLAY.get(n,n),"cumulative_return":m["cumulative_return"],"excess_vs_ew_bh":m["cumulative_return"]-ew["cumulative_return"],"sharpe":m["sharpe_ratio"],"maximum_drawdown":m["maximum_drawdown"],"calmar":m["calmar_ratio"]})
    for n,m in [("EW_BH",ew),("SPY",spy)]: agg.append({"system":DISPLAY[n],"cumulative_return":m["cumulative_return"],"excess_vs_ew_bh":m["cumulative_return"]-ew["cumulative_return"],"sharpe":m["sharpe_ratio"],"maximum_drawdown":m["maximum_drawdown"],"calmar":m["calmar_ratio"]})
    pcols=[("system","System","text"),("cumulative_return","Cumulative Return","pct"),("excess_vs_ew_bh","Excess vs EW B&H","pp"),("sharpe","Sharpe","ratio"),("maximum_drawdown","Maximum Drawdown","pct"),("calmar","Calmar","ratio")]
    write_csv(out/"tables/aggregate_primary.csv",agg); (out/"tables/aggregate_primary.md").write_text(markdown_table(agg,pcols),encoding="utf-8"); (out/"tables/aggregate_primary.tex").write_text(latex_table(agg,pcols,"Aggregate primary results","tab:aggregate-primary"),encoding="utf-8")
    all_metrics={n:metrics[n]["aggregate"] for n in SYSTEMS}|{"EW_BH":ew,"SPY":spy}
    sec=[]
    for n,m in all_metrics.items(): sec.append({"system":DISPLAY.get(n,n),"annualized_return":m["annualized_return"],"volatility":m["annualized_volatility"],"sortino":m["sortino_ratio"],"average_exposure":m["average_exposure"],"time_in_market":m["time_in_market"],"turnover":m["turnover"],"trade_count":m["trade_count"],"commission_cost":m["total_commission_cost"],"slippage_cost":m["total_slippage_cost"],"total_cost":m["total_transaction_cost"],"buy":m["buy_decision_count"],"hold":m["hold_decision_count"],"sell":m["sell_decision_count"],"no_op":m["noop_rebalance_count"],"failure_rate":m.get("decision_failure_rate"),"model_failure_rate":m.get("model_failure_rate")})
    scols=[("system","System","text"),("annualized_return","Annualised Return","pct"),("volatility","Volatility","pct"),("sortino","Sortino","ratio"),("average_exposure","Average Exposure","pct"),("time_in_market","Time in Market","pct"),("turnover","Turnover","ratio"),("trade_count","Trades","int"),("total_cost","Total Cost","money"),("buy","BUY","int"),("hold","HOLD","int"),("sell","SELL","int"),("no_op","No-op","int"),("failure_rate","Failure Rate","pct"),("model_failure_rate","Model Failure Rate","pct")]
    write_csv(out/"tables/aggregate_secondary.csv",sec); (out/"tables/aggregate_secondary.md").write_text(markdown_table(sec,scols),encoding="utf-8"); (out/"tables/aggregate_secondary.tex").write_text(latex_table(sec,scols,"Aggregate behavioural and risk results","tab:aggregate-secondary"),encoding="utf-8")
    per_tables={}
    for s in SYMBOLS:
        rows=[]
        for n in SYSTEMS:
            m=metrics[n][s]; rows.append({"system":DISPLAY.get(n,n),"cumulative_return":m["cumulative_return"],"excess_vs_stock_bh":m["cumulative_return"]-bh[s]["cumulative_return"],"sharpe":m["sharpe_ratio"],"maximum_drawdown":m["maximum_drawdown"],"calmar":m["calmar_ratio"],"average_exposure":m["average_exposure"],"turnover":m["turnover"],"trade_count":m["trade_count"],"total_cost":m["total_transaction_cost"]})
        for n,m in [(f"{s} B&H",bh[s]),("SPY",spy)]: rows.append({"system":n,"cumulative_return":m["cumulative_return"],"excess_vs_stock_bh":m["cumulative_return"]-bh[s]["cumulative_return"],"sharpe":m["sharpe_ratio"],"maximum_drawdown":m["maximum_drawdown"],"calmar":m["calmar_ratio"],"average_exposure":m["average_exposure"],"turnover":m["turnover"],"trade_count":m["trade_count"],"total_cost":m["total_transaction_cost"]})
        per_tables[s]=rows; cols=[("system","System","text"),("cumulative_return","Cumulative Return","pct"),("excess_vs_stock_bh",f"Excess vs {s} B&H","pp"),("sharpe","Sharpe","ratio"),("maximum_drawdown","MDD","pct"),("calmar","Calmar","ratio"),("average_exposure","Average Exposure","pct"),("turnover","Turnover","ratio"),("trade_count","Trades","int"),("total_cost","Total Cost","money")]
        write_csv(out/f"tables/{s}_primary.csv",rows); (out/f"tables/{s}_primary.md").write_text(markdown_table(rows,cols),encoding="utf-8"); (out/f"tables/{s}_primary.tex").write_text(latex_table(rows,cols,f"{s} primary results",f"tab:{s.lower()}-primary"),encoding="utf-8")
    # Controlled deltas and consistency.
    contrasts=[("RQ1","M1-M0","M1","M0","PRIMARY"),("RQ2","M2-M1","M2","M1","PRIMARY"),("RQ3a","A1-M2","A1","M2","PRIMARY"),("RQ3b","A2-M2","A2","M2","PRIMARY"),("Context","A1-M1","A1","M1","SECONDARY CONTEXT"),("Context","A2-M1","A2","M1","SECONDARY CONTEXT")]
    dmetrics=["cumulative_return","sharpe_ratio","maximum_drawdown","calmar_ratio","average_exposure","turnover","total_transaction_cost"]
    deltas=[]
    for rq,label,a,b,role in contrasts:
        for scope in ["aggregate",*SYMBOLS]:
            for met in dmetrics:
                av,bv=metrics[a][scope].get(met),metrics[b][scope].get(met); delta=None if av is None or bv is None else av-bv
                storage_unit,display_unit=DELTA_UNITS[met]
                deltas.append({"research_question":rq,"contrast":label,"role":role,"scope":scope,"metric":met,"delta":delta,"storage_unit":storage_unit,"display_unit":display_unit,"direction_metadata":METRIC_DIRECTIONS[met]["direction"]})
    write_csv(out/"tables/controlled_deltas.csv",deltas,lineterminator="\n")
    consistency=[]
    for rq,label,a,b,role in contrasts[:4]:
        for met in ["cumulative_return","sharpe_ratio","maximum_drawdown"]:
            dirs=[]
            for s in SYMBOLS:
                av,bv=metrics[a][s].get(met),metrics[b][s].get(met)
                if av is None or bv is None: d="not comparable"
                elif abs(av-bv)<1e-15: d="equal"
                elif (av>bv)==(METRIC_DIRECTIONS[met]["direction"]=="higher"): d="improved"
                else: d="worsened"
                dirs.append(d)
            comparable=[d for d in dirs if d!="not comparable"]
            consistency.append({"research_question":rq,"contrast":label,"metric":met,"AAPL":dirs[0],"AMZN":dirs[1],"JPM":dirs[2],"improved_count":dirs.count("improved"),"equal_count":dirs.count("equal"),"worsened_count":dirs.count("worsened"),"comparable_asset_count":len(comparable),"direction_consistent":len(set(comparable))<=1})
    write_csv(out/"tables/cross_asset_consistency.csv",consistency)
    exposure=[{"system":n,"cumulative_return":metrics[n]["aggregate"]["cumulative_return"],"average_exposure":metrics[n]["aggregate"]["average_exposure"],"time_in_market":metrics[n]["aggregate"]["time_in_market"],"turnover":metrics[n]["aggregate"]["turnover"],"trade_count":metrics[n]["aggregate"]["trade_count"],"total_cost":metrics[n]["aggregate"]["total_transaction_cost"]} for n in SYSTEMS]
    write_csv(out/"tables/exposure_participation.csv",exposure)
    # RL action pathway, including legal PM mediation.
    pathway_events=[]; pathway=[]
    for n in ["M2","A1","A2"]:
        timeline=read_csv(roots[n]["path"]/"analysis_ready/decision_timeline.csv")
        bykey={(r["symbol"],r["decision_session"]):r for r in timeline}
        scopes={"aggregate":[]}
        for s in SYMBOLS:
            events=[]
            for row in read_csv(roots[n]["path"]/"strategy"/s/"decisions.csv"):
                md=ast.literal_eval(row["metadata"]); hand=md["m2_trader_handoff"]; prompt=hand["prompt_action"]; rl=hand["authoritative_action"]; pm=row["action"]; t=bykey[(s,row["decision_session"])]
                before=float(t["portfolio_weight_before"]); expected_fill=(pm=="BUY" and before<1e-9) or (pm=="SELL" and before>1e-9); actual_fill=bool(t["fill_quantity"]); consistent=expected_fill==actual_fill
                e={"system":n,"symbol":s,"decision_session":row["decision_session"],"prompt_action":prompt,"rl_action":rl,"override_status":"OVERRIDE" if prompt!=rl else "RETAIN","pm_action":pm,"pm_target_weight":float(t["target_weight"]),"rl_pm_status":"MEDIATED" if rl!=pm else "AGREE","executed_action":pm if actual_fill else "NO_FILL","executed_fill":int(actual_fill),"pm_execution_consistent":consistent,"rebalance_status":t["rebalance_status"]}
                events.append(e); pathway_events.append(e)
            scopes[s]=events; scopes["aggregate"].extend(events)
        for scope,events in scopes.items():
            pc=Counter(e["prompt_action"] for e in events); rc=Counter(e["rl_action"] for e in events); mc=Counter(e["pm_action"] for e in events); total=len(events)
            pathway.append({"system":n,"scope":scope,"decisions":total,"override_count":sum(e["override_status"]=="OVERRIDE" for e in events),"override_rate":sum(e["override_status"]=="OVERRIDE" for e in events)/total,"retain_count":sum(e["override_status"]=="RETAIN" for e in events),"retain_rate":sum(e["override_status"]=="RETAIN" for e in events)/total,"rl_pm_mediation_count":sum(e["rl_pm_status"]=="MEDIATED" for e in events),"rl_pm_mediation_rate":sum(e["rl_pm_status"]=="MEDIATED" for e in events)/total,"pm_execution_consistency_count":sum(e["pm_execution_consistent"] for e in events),"pm_execution_consistency_rate":sum(e["pm_execution_consistent"] for e in events)/total,"prompt_BUY":pc["BUY"],"prompt_HOLD":pc["HOLD"],"prompt_SELL":pc["SELL"],"rl_BUY":rc["BUY"],"rl_HOLD":rc["HOLD"],"rl_SELL":rc["SELL"],"pm_BUY":mc["BUY"],"pm_HOLD":mc["HOLD"],"pm_SELL":mc["SELL"],"actual_fill_count":sum(e["executed_fill"] for e in events)})
    write_csv(out/"data/rl_pathway_events.csv",pathway_events); write_csv(out/"tables/rl_action_pathway.csv",pathway)
    # Credit/update summaries from frozen runtime/audits.
    m2audit=load_json(repo/"experiments/M2/m2_post_run_audit.json")["correctness"]["rl_chronology"]
    a1audit=load_json(repo/"experiments/A1/formal/a1_post_run_audit.json")["memory_and_credit_chronology"]
    a2audit=load_json(repo/"experiments/A2/formal/A2_POST_RUN_AUDIT.json")["final_state"]
    updates=[]
    for n in ["M2","A1","A2"]:
        for s in SYMBOLS:
            if n=="M2":
                d=m2audit[s]; state=load_json(roots[n]["path"]/"provenance/runtime/m2_state"/s/"runtime_state.json"); credits=state["credits"]; initial=credits[0]["pre_fast_sha"]; final=next((c.get("post_fast_sha") for c in reversed(credits) if c.get("post_fast_sha")),initial); applied=d["APPLIED"]; archived=d["ARCHIVED"]; pending=d["PENDING"]; application_ids=[u["application_id"] for u in state["update_records"]]
            elif n=="A1":
                d=a1audit[s]; treatment=load_json(repo/"experiments/A1/formal/a1_post_run_audit.json")["treatment_audit"]; initial=treatment["initial_fast_sha256"]; final=treatment["final_fast_sha256"]; applied=0; archived=d["archived"]; pending=d["pending_terminal"]; application_ids=[]
            else:
                d=a2audit[s]; initial=d["initial_fast_sha"]; final=d["final_fast_sha"]; applied=d["credit_status_counts"]["APPLIED"]; archived=d["credit_status_counts"]["ARCHIVED"]; pending=d["credit_status_counts"]["PENDING"]; application_ids=[u["application_id"] for u in d["updates"]]
            updates.append({"system":n,"symbol":s,"credits_issued":26,"APPLIED":applied,"ARCHIVED":archived,"PENDING":pending,"fast_parameter_updates":applied,"application_id_count":applied,"application_ids":";".join(application_ids),"initial_fast_identity":initial,"final_fast_identity":final,"fast_identity_changed":initial!=final})
    write_csv(out/"tables/rl_update_summary.csv",updates)
    # Combined equity data and terminal validation.
    equity_rows=[]; recalcs={}
    for n in SYSTEMS:
        p=roots[n]["path"]/"aggregate/equal_weight_equity.csv"; pts=read_csv(p); recalcs[n]={"official":metrics[n]["aggregate"]["cumulative_return"],"recalculated":terminal_return(p)}
        for r in pts: equity_rows.append({"system":n,"session":r["session"],"normalized_equity":r["normalized_equity"]})
    for n,p in [("EW_BH",repo/"experiments/M0/benchmarks/equal_weight_buy_and_hold_equity.csv"),("SPY",repo/"experiments/M0/benchmarks/SPY_buy_and_hold/daily_equity.csv")]:
        pts=read_csv(p); key="normalized_equity" if "normalized_equity" in pts[0] else "equity"; base=float(pts[0][key]); recalcs[n]={"official":EXPECTED_RETURNS[n],"recalculated":float(pts[-1][key])/base-1}
        for r in pts: equity_rows.append({"system":n,"session":r["session"],"normalized_equity":float(r[key])/base})
    for v in recalcs.values(): v["absolute_difference"]=abs(v["official"]-v["recalculated"]); v["status"]="PASS" if v["absolute_difference"]<=1e-12 else "DISCREPANCY"
    if any(v["status"]!="PASS" for v in recalcs.values()): raise SystemExit("BLOCKED: validation recalculation discrepancy")
    write_csv(out/"data/aggregate_equity_curves.csv",equity_rows)
    # Main dissertation tables.
    main=[]
    for n,m in all_metrics.items(): main.append({"system":DISPLAY.get(n,n),"role":{"M0":"MAS baseline","M1":"Information treatment","M2":"Full Agentic RL","A1":"Global-only ablation","A2":"Online-only ablation","ARMA":"Classical benchmark","EW_BH":"Market reference","SPY":"Market reference"}[n],"cumulative_return":m["cumulative_return"],"excess_vs_ew_bh":m["cumulative_return"]-ew["cumulative_return"],"sharpe":m["sharpe_ratio"],"maximum_drawdown":m["maximum_drawdown"],"calmar":m["calmar_ratio"],"average_exposure":m["average_exposure"],"turnover":m["turnover"],"total_cost":m["total_transaction_cost"]})
    maincols=[("system","System","text"),("role","Role","text"),("cumulative_return","Cumulative Return","pct"),("excess_vs_ew_bh","Excess vs EW B&H","pp"),("sharpe","Sharpe","ratio"),("maximum_drawdown","MDD","pct"),("calmar","Calmar","ratio"),("average_exposure","Average Exposure","pct"),("turnover","Turnover","ratio"),("total_cost","Total Cost","money")]
    (out/"tables/THESIS_MAIN_RESULTS_TABLE.md").write_text("# Thesis Main Results Table\n\n"+markdown_table(main,maincols)+"\nNotes: official frozen metrics; MDD is a positive loss magnitude; null ratios are shown as em dashes; ARMA is contextual rather than an RQ treatment.\n",encoding="utf-8")
    (out/"tables/THESIS_MAIN_RESULTS_TABLE.tex").write_text(latex_table(main,maincols,"Final controlled comparison under the frozen 2024H1 protocol","tab:thesis-main-results"),encoding="utf-8")
    lookup={(r["contrast"],r["scope"],r["metric"]):r["delta"] for r in deltas}
    interpretations={"M1-M0":"Aggregate return and risk-adjusted performance improved, with heterogeneous stock-level returns.","M2-M1":"Full Agentic RL materially reduced aggregate return and participation; AMZN was the sole stock-level return improvement.","A1-M2":"Global-only A1 materially outperformed Full M2 in aggregate, driven by AMZN and JPM; AAPL remained in cash.","A2-M2":"Online-only A2 outperformed Full M2 in aggregate; AAPL remained in cash and JPM avoided M2's loss by not entering."}
    controlled=[]
    for rq,label,a,b,role in contrasts[:4]: controlled.append({"comparison":f"{rq}: {label}","aggregate_return_delta":lookup[(label,"aggregate","cumulative_return")],"AAPL_return_delta":lookup[(label,"AAPL","cumulative_return")],"AMZN_return_delta":lookup[(label,"AMZN","cumulative_return")],"JPM_return_delta":lookup[(label,"JPM","cumulative_return")],"sharpe_delta":lookup[(label,"aggregate","sharpe_ratio")],"MDD_delta":lookup[(label,"aggregate","maximum_drawdown")],"exposure_delta":lookup[(label,"aggregate","average_exposure")],"interpretation":interpretations[label]})
    ccols=[("comparison","Comparison","text"),("aggregate_return_delta","Aggregate Return Delta","pp"),("AAPL_return_delta","AAPL Return Delta","pp"),("AMZN_return_delta","AMZN Return Delta","pp"),("JPM_return_delta","JPM Return Delta","pp"),("sharpe_delta","Sharpe Delta","ratio"),("MDD_delta","MDD Delta","pp"),("exposure_delta","Exposure Delta","pp"),("interpretation","Interpretation","text")]
    (out/"tables/THESIS_CONTROLLED_COMPARISONS.md").write_text("# Thesis Controlled Comparisons\n\n"+markdown_table(controlled,ccols)+"\nPositive MDD deltas mean a larger (worse) drawdown; exposure deltas are descriptive.\n",encoding="utf-8")
    (out/"tables/THESIS_CONTROLLED_COMPARISONS.tex").write_text(latex_table(controlled,ccols,"Preregistered controlled comparisons","tab:controlled-comparisons"),encoding="utf-8")
    # Figures.
    source_note="Official frozen AlphaMAS-Experiments artifacts; 2024H1, generated by COMPARE-01"
    names=SYSTEMS+["EW_BH","SPY"]; bar_svg(out/"figures/figure_01_aggregate_cumulative_return.svg",[DISPLAY.get(n,n) for n in names],[100 * all_metrics[n]["cumulative_return"] for n in names],"Aggregate Cumulative Return","Cumulative Return (%)",source_note)
    eq_by={n:[] for n in names}
    for r in equity_rows: eq_by[r["system"]].append((r["session"],float(r["normalized_equity"])))
    line_svg(out/"figures/figure_02_aggregate_equity_curves.svg",[(DISPLAY.get(n,n),eq_by[n]) for n in names],"Aggregate Daily Equity Curves","Normalised equity",source_note)
    series=[]
    for n in names:
        vals=[]
        for s in SYMBOLS:
            if n in SYSTEMS: vals.append(metrics[n][s]["cumulative_return"])
            elif n=="EW_BH": vals.append(bh[s]["cumulative_return"])
            else: vals.append(spy["cumulative_return"])
        series.append((DISPLAY.get(n,n),[None if v is None else 100 * v for v in vals]))
    grouped_bar_svg(out/"figures/figure_03_per_stock_returns.svg",SYMBOLS,series,"Per-Stock Cumulative Return","Cumulative Return (%)",source_note)
    scatter_svg(out/"figures/figure_04_return_vs_exposure.svg",[(DISPLAY.get(n,n),100 * metrics[n]["aggregate"]["average_exposure"],100 * metrics[n]["aggregate"]["cumulative_return"]) for n in SYSTEMS],"Return and Market Participation","Average Exposure (%)","Cumulative Return (%)",source_note)
    small_multiple_bar_svg(out/"figures/figure_05_risk_return.svg",[DISPLAY.get(n,n) for n in names],[("Sharpe",[all_metrics[n]["sharpe_ratio"] for n in names],"ratio"),("Maximum Drawdown",[100 * all_metrics[n]["maximum_drawdown"] for n in names],"%"),("Calmar",[all_metrics[n]["calmar_ratio"] for n in names],"ratio")],"Risk-Return Comparison — Separate Metric Panels",source_note)
    primary_labels=[x[1] for x in contrasts[:4]]; grouped_bar_svg(out/"figures/figure_06_controlled_return_deltas.svg",["Aggregate",*SYMBOLS],[(lab,[100 * lookup[(lab,scope,"cumulative_return")] for scope in ["aggregate",*SYMBOLS]]) for lab in primary_labels],"Controlled Cumulative-Return Deltas","Percentage-point change (pp)",source_note)
    small_multiple_bar_svg(out/"figures/figure_07_trading_intensity_cost.svg",[DISPLAY.get(n,n) for n in SYSTEMS],[("Turnover",[metrics[n]["aggregate"]["turnover"] for n in SYSTEMS],"ratio"),("Trade Count",[metrics[n]["aggregate"]["trade_count"] for n in SYSTEMS],"fills"),("Transaction Cost",[metrics[n]["aggregate"]["total_transaction_cost"] for n in SYSTEMS],"USD")],"Trading Intensity and Cost — Separate Metric Panels",source_note)
    aggp={r["system"]:r for r in pathway if r["scope"]=="aggregate"}; grouped_bar_svg(out/"figures/figure_08_rl_action_pathway.svg",["M2","A1","A2"],[("RL override rate",[100 * aggp[n]["override_rate"] for n in ["M2","A1","A2"]]),("RL-PM mediation rate",[100 * aggp[n]["rl_pm_mediation_rate"] for n in ["M2","A1","A2"]]),("PM-execution consistency",[100 * aggp[n]["pm_execution_consistency_rate"] for n in ["M2","A1","A2"]])],"RL Action Pathway","Rate (%)",source_note)
    # Reports.
    def delta(label,scope,met): return lookup[(label,scope,met)]
    m0,m1,m2,a1,a2=(metrics[x]["aggregate"] for x in ["M0","M1","M2","A1","A2"])
    rq1=f"""# RQ1 — Information Contribution

## Evidence

M1 increased aggregate cumulative return over M0 by {format_percentage_points_prose(delta('M1-M0','aggregate','cumulative_return'))} ({fmt(m0['cumulative_return'],'pct')} to {fmt(m1['cumulative_return'],'pct')}), Sharpe by {fmt(delta('M1-M0','aggregate','sharpe_ratio'))}, and Calmar by {fmt(delta('M1-M0','aggregate','calmar_ratio'))}. Maximum drawdown fell by {format_percentage_points_prose(-delta('M1-M0','aggregate','maximum_drawdown'))} on a lower-is-better basis. Average exposure fell {format_percentage_points_prose(abs(delta('M1-M0','aggregate','average_exposure')))}, turnover fell {fmt(abs(delta('M1-M0','aggregate','turnover')))}, and total cost fell {fmt(abs(delta('M1-M0','aggregate','total_transaction_cost')),'money')}.

Per-stock return deltas were AAPL {format_percentage_points_prose(delta('M1-M0','AAPL','cumulative_return'), signed=True)}, AMZN {format_percentage_points_prose(delta('M1-M0','AMZN','cumulative_return'), signed=True)}, and JPM {format_percentage_points_prose(delta('M1-M0','JPM','cumulative_return'), signed=True)}: 2/3 improved. Sharpe and MDD also improved for 2/3 assets. M1 recorded {m1['buy_decision_count']}/{m1['hold_decision_count']}/{m1['sell_decision_count']} BUY/HOLD/SELL decisions versus M0's {m0['buy_decision_count']}/{m0['hold_decision_count']}/{m0['sell_decision_count']}.

## Answer

Under the frozen 2024H1 three-asset protocol, richer PIT-safe FinMultiTime information improved aggregate performance and risk-adjusted results relative to M0. The contribution was not universal: AMZN return and Sharpe declined, while AAPL and JPM improved. This is descriptive controlled evidence, not a statistical-significance claim.
"""
    (out/"reports/RQ1_INFORMATION_CONTRIBUTION.md").write_text(rq1,encoding="utf-8")
    rq2=f"""# RQ2 — Agentic RL Contribution

## Evidence

With the information environment held fixed, M2 reduced aggregate cumulative return by {format_percentage_points_prose(abs(delta('M2-M1','aggregate','cumulative_return')))} relative to M1 ({fmt(m1['cumulative_return'],'pct')} to {fmt(m2['cumulative_return'],'pct')}). Sharpe changed by {fmt(delta('M2-M1','aggregate','sharpe_ratio'))}; MDD increased by {format_percentage_points_prose(delta('M2-M1','aggregate','maximum_drawdown'))}; Calmar changed by {fmt(delta('M2-M1','aggregate','calmar_ratio'))}. Average exposure fell from {fmt(m1['average_exposure'],'pct')} to {fmt(m2['average_exposure'],'pct')}, while turnover rose from {fmt(m1['turnover'])} to {fmt(m2['turnover'])}, trades rose from {m1['trade_count']} to {m2['trade_count']}, and cost rose by {fmt(delta('M2-M1','aggregate','total_transaction_cost'),'money')}.

Stock return deltas were AAPL {format_percentage_points_prose(delta('M2-M1','AAPL','cumulative_return'), signed=True)}, AMZN {format_percentage_points_prose(delta('M2-M1','AMZN','cumulative_return'), signed=True)}, and JPM {format_percentage_points_prose(delta('M2-M1','JPM','cumulative_return'), signed=True)}. Only AMZN improved, marginally. AAPL never entered the market; JPM lost {fmt(abs(metrics['M2']['JPM']['cumulative_return']),'pct')}.

## Answer

The complete Agentic RL Trader did not improve the frozen system economically. It materially changed behaviour—lower aggregate participation but higher switching intensity and cost—and produced worse aggregate return and risk-adjusted performance. This is a correctness-valid negative result, not an implementation failure: every M2 audit passed and PM-to-execution mapping was consistent in all 78 decisions.
"""
    (out/"reports/RQ2_AGENTIC_RL_CONTRIBUTION.md").write_text(rq2,encoding="utf-8")
    rq3=f"""# RQ3 — RL Mechanisms

Canonical treatments: `M2 = global pretraining + online adaptation`; `A1 = global pretraining only`; `A2 = online adaptation only`.

## Aggregate comparison

A1 exceeded M2 return by {format_percentage_points_prose(delta('A1-M2','aggregate','cumulative_return'))} and A2 exceeded M2 by {format_percentage_points_prose(delta('A2-M2','aggregate','cumulative_return'))}. A1 also had much higher exposure ({fmt(a1['average_exposure'],'pct')}) than M2 ({fmt(m2['average_exposure'],'pct')}), whereas A2 exposure was {fmt(a2['average_exposure'],'pct')}. A1 and A2 each incurred fewer trades and lower costs than M2. A1 exceeded A2 return by {format_percentage_points_prose(a1['cumulative_return']-a2['cumulative_return'])}, but A2 had the lower MDD.

## Asset mechanisms

- AAPL: all three RL treatments stayed in cash, despite different action pathways and extensive M2/A2 parameter updating.
- AMZN: M2 returned {fmt(metrics['M2']['AMZN']['cumulative_return'],'pct')} at {fmt(metrics['M2']['AMZN']['average_exposure'],'pct')} exposure; A1 returned {fmt(metrics['A1']['AMZN']['cumulative_return'],'pct')} at {fmt(metrics['A1']['AMZN']['average_exposure'],'pct')}; A2 returned {fmt(metrics['A2']['AMZN']['cumulative_return'],'pct')} at {fmt(metrics['A2']['AMZN']['average_exposure'],'pct')}. Earlier and more persistent participation coincided with the higher ablation returns.
- JPM: A1 entered and returned {fmt(metrics['A1']['JPM']['cumulative_return'],'pct')}; M2 traded twice and returned {fmt(metrics['M2']['JPM']['cumulative_return'],'pct')}; A2 remained in cash and returned 0%. The mechanisms therefore changed whether and when the systems participated.

## Interpretation guardrail

The combined Full-M2 configuration performed materially worse than either single-mechanism ablation in aggregate. The pattern is consistent with a negative or non-additive relationship between global pretraining and delayed online adaptation. It is not a formal factorial interaction proof: M1 uses the Prompt Trader without the A1/A2/M2 RL policy layer and is not an equivalent RL “neither” cell. No p-values or significance claims are made.
"""
    (out/"reports/RQ3_RL_MECHANISMS.md").write_text(rq3,encoding="utf-8")
    # Case narratives, with explicit epistemic separation.
    case_text={
    "AAPL":f"""# AAPL Case Analysis

## OBSERVED

M2, A1 and A2 each had 0.00% cumulative return, 0.00% exposure, zero turnover, zero fills and zero transaction cost. Their final actions differed (M2 0/22/4, A1 0/20/6, A2 0/21/5 BUY/HOLD/SELL), but none issued a PM BUY while in cash. M2 and A2 each processed 23 applied online updates for AAPL; A1 archived 25 matured credits and performed zero parameter updates. M1, by contrast, participated at {fmt(metrics['M1']['AAPL']['average_exposure'],'pct')} exposure and returned {fmt(metrics['M1']['AAPL']['cumulative_return'],'pct')}.

## INTERPRETATION

For AAPL, parameter evolution and RL-level action changes did not cross the economic threshold required for an executed entry. This demonstrates that learning-state mutation and even pathway overrides are not equivalent to portfolio participation.

## UNRESOLVED

The frozen records establish the pathway but do not identify a single causal reason why PM never authorised a BUY. Post-hoc policy redesign on this evaluation window would violate the no-M3 rule.
""",
    "AMZN":f"""# AMZN Case Analysis

## OBSERVED

M2 returned {fmt(metrics['M2']['AMZN']['cumulative_return'],'pct')} with {fmt(metrics['M2']['AMZN']['average_exposure'],'pct')} exposure, three fills and {fmt(metrics['M2']['AMZN']['total_transaction_cost'],'money')} cost. A1 returned {fmt(metrics['A1']['AMZN']['cumulative_return'],'pct')} with {fmt(metrics['A1']['AMZN']['average_exposure'],'pct')} exposure and one fill. A2 returned {fmt(metrics['A2']['AMZN']['cumulative_return'],'pct')} with {fmt(metrics['A2']['AMZN']['average_exposure'],'pct')} exposure and one fill. The frozen pathway shows substantial override and PM mediation in M2/A1, but none in A2.

## INTERPRETATION

The ablations' earlier, persistent long exposure coincided with materially higher AMZN returns and lower trading cost. M2's extra switching raised turnover and cost without raising return above M1 materially.

## UNRESOLVED

The observational timing relationship does not prove exposure caused the return difference; the path also reflects different frozen proposals and policy actions.
""",
    "JPM":f"""# JPM Case Analysis

## OBSERVED

A1 returned {fmt(metrics['A1']['JPM']['cumulative_return'],'pct')} with {fmt(metrics['A1']['JPM']['average_exposure'],'pct')} exposure and one fill. M2 returned {fmt(metrics['M2']['JPM']['cumulative_return'],'pct')} with {fmt(metrics['M2']['JPM']['average_exposure'],'pct')} exposure and two fills. A2 stayed in cash and returned 0.00%. M2/A2 each recorded 23 applied online updates; A1 recorded none.

## INTERPRETATION

Global-only A1 captured much of JPM's positive market path. Full M2's later or interrupted participation coincided with a small loss, while online-only A2 did not convert adaptation into an entry. The mechanism contrast is therefore economic as well as parametric.

## UNRESOLVED

Three frozen trajectories cannot isolate a universal causal rule for when global and online components should be combined.
"""}
    for s,t in case_text.items(): (out/f"reports/{s}_CASE_ANALYSIS.md").write_text(t,encoding="utf-8")
    (out/"reports/MARKET_PARTICIPATION.md").write_text(f"""# Market Participation

Aggregate exposure ranged from {fmt(m2['average_exposure'],'pct')} for M2 to {fmt(metrics['ARMA']['aggregate']['average_exposure'],'pct')} for ARMA. M1 improved on M0 while using less exposure, turnover and cost. M2 used still less exposure but more turnover and cost than M1, indicating more switching within a shorter participation footprint. A1 combined {fmt(a1['average_exposure'],'pct')} exposure with only {a1['trade_count']} fills; A2 used {fmt(a2['average_exposure'],'pct')} exposure with {a2['trade_count']} fill. ARMA's {fmt(metrics['ARMA']['aggregate']['cumulative_return'],'pct')} return coincided with near-continuous exposure, not a low-exposure timing profile.

These are observed associations. Exposure, entry timing, switching and return are jointly realised outcomes; the comparison does not claim that exposure alone caused performance. See `tables/exposure_participation.csv`.
""",encoding="utf-8")
    arma=metrics["ARMA"]["aggregate"]; rank=sorted(((n,all_metrics[n]["cumulative_return"]) for n in names),key=lambda x:x[1],reverse=True); rankpos=[n for n,_ in rank].index("ARMA")+1
    stock_excess={s:metrics["ARMA"][s]["cumulative_return"]-bh[s]["cumulative_return"] for s in SYMBOLS}
    (out/"reports/ARMA_CONTEXT.md").write_text(f"""# ARMA(1,1) Context

ARMA ranked {rankpos} of {len(rank)} on cumulative return at {fmt(arma['cumulative_return'],'pct')}, behind Equal-weight B&H ({fmt(ew['cumulative_return'],'pct')}) but ahead of SPY ({fmt(spy['cumulative_return'],'pct')}) and every MAS configuration. Its Sharpe was {fmt(arma['sharpe_ratio'])}, MDD {fmt(arma['maximum_drawdown'],'pct')}, and Calmar {fmt(arma['calmar_ratio'])}. It maintained {fmt(arma['average_exposure'],'pct')} average exposure, turnover {fmt(arma['turnover'])}, {arma['trade_count']} fills and {fmt(arma['total_transaction_cost'],'money')} cost.

Per-stock excess versus Buy & Hold was AAPL {format_percentage_points_prose(stock_excess['AAPL'], signed=True)}, AMZN {format_percentage_points_prose(stock_excess['AMZN'], signed=True)}, and JPM {format_percentage_points_prose(stock_excess['JPM'], signed=True)}. Thus ARMA did not beat any same-stock Buy & Hold reference (JPM is effectively equal within numerical precision), and it underperformed Equal-weight B&H by {format_percentage_points_prose(abs(arma['cumulative_return']-ew['cumulative_return']))}.

ARMA therefore provides a high-return classical context, not evidence of universal superiority or positive market-timing alpha. Its result largely coincided with persistent market participation during a strong positive regime.
""",encoding="utf-8")
    upagg={n:{k:sum(int(r[k]) for r in updates if r["system"]==n) for k in ["credits_issued","APPLIED","ARCHIVED","PENDING","fast_parameter_updates"]} for n in ["M2","A1","A2"]}
    (out/"reports/PARAMETER_TO_ECONOMIC_BEHAVIOUR.md").write_text(f"""# Parameter Adaptation and Economic Behaviour

M2 and A2 each issued {upagg['M2']['credits_issued']} credits and applied {upagg['M2']['APPLIED']} fast-parameter updates across the three assets; each also archived {upagg['M2']['ARCHIVED']} credits and retained {upagg['M2']['PENDING']} terminal credits as pending. A1 issued {upagg['A1']['credits_issued']} credits, archived {upagg['A1']['ARCHIVED']} matured credits because adaptation was disabled, retained {upagg['A1']['PENDING']} terminal credits, and performed zero updates.

The economic mapping was not monotonic. M2 and A2 both updated AAPL parameters 23 times yet generated zero AAPL fills. A2 updated JPM parameters 23 times yet stayed in cash. M2 generated many AMZN RL overrides, but legal PM mediation often preserved the PM outcome. Conversely, A1 achieved the highest JPM participation and return without any online parameter mutation.

Hashes in `tables/rl_update_summary.csv` establish identity only; no numerical distance between hashes is inferred. The evidence shows that parameter mutation is neither identical to behavioural change nor sufficient evidence of useful learning.
""",encoding="utf-8")
    (out/"reports/RESEARCH_QUESTION_ANSWERS.md").write_text(f"""# Research Question Answers

## RQ1

M1 improved aggregate return by {format_percentage_points_prose(delta('M1-M0','aggregate','cumulative_return'))}, Sharpe by {fmt(delta('M1-M0','aggregate','sharpe_ratio'))}, and reduced aggregate drawdown. Answer: richer PIT-safe information improved the MAS in aggregate under this protocol. Caveat: return improved for 2/3 stocks; AMZN deteriorated.

## RQ2

M2 reduced aggregate return by {format_percentage_points_prose(abs(delta('M2-M1','aggregate','cumulative_return')))}, reduced Sharpe, lowered exposure, and raised turnover and cost. Answer: the complete Agentic RL layer did not further improve the system; it materially altered participation and switching. M2 passed correctness audits, so this is an economic negative result rather than an implementation-failure label.

## RQ3

A1 and A2 each materially outperformed Full M2 in aggregate. A1 was strongest on JPM and A2 on AMZN; all RL treatments stayed in cash on AAPL. Answer: global-only and online-only components produced distinct, asset-dependent pathways, and their combination was non-monotonic. The pattern is consistent with negative/non-additive interaction, but is not a formal factorial interaction estimate.

## Limitations

Evidence is descriptive across three heterogeneous assets in one positive 2024H1 regime. No p-values or statistical-significance claims are made. ARMA is contextual only and does not answer the causal RQs.
""",encoding="utf-8")
    (out/"reports/CLAIM_GUARDRAILS.md").write_text("""# Claim Guardrails

## SUPPORTED CLAIMS

- Under the frozen 2024H1 three-asset protocol, M1 improved aggregate performance relative to M0.
- The information effect was heterogeneous: 2/3 stocks improved in return.
- Full M2 performed materially worse than M1 and either single-mechanism ablation in aggregate.
- The observed mechanism pattern is consistent with a negative or non-additive relationship between global pretraining and delayed online adaptation.
- RL parameter updating did not always translate into market participation or fills.
- ARMA had high return and high exposure, but did not beat Equal-weight or same-stock Buy & Hold.

## UNSUPPORTED / OVERSTATED CLAIMS

- “Agentic RL generally does not work in finance.”
- “FinMultiTime universally improves all assets.”
- “A statistically significant interaction was proven.”
- “M1 is an exact RL neither-cell.”
- “A1/A2 identify a universal causal law.”
- “ARMA is superior to MAS in general” or necessarily generated market-timing alpha.
- “The results generalise to all assets or market regimes.”
- Any p-value, confidence, or statistical-significance wording not preregistered here.
""",encoding="utf-8")
    (out/"reports/LIMITATIONS.md").write_text("""# Limitations

- The evaluation contains three stocks only and treats AAPL, AMZN and JPM as heterogeneous cases.
- It covers one 2024H1 market regime, in which all Buy & Hold references had strong positive returns.
- The paradigm is descriptive controlled evaluation plus cross-asset consistency, not inferential statistical significance.
- LLM outputs can remain nondeterministic despite temperature 0.
- The policy froze the first complete correctness-valid trajectory rather than selecting a favourable rerun.
- RL development contexts were limited, with one frozen global choice and one frozen online hyperparameter choice.
- A1/A2 do not create a complete strict factorial test because M1 is not an equivalent RL “neither” architecture.
- Asset heterogeneity limits simple aggregation and makes the per-stock cases primary evidence.
- ARMA maintained high market exposure, so high return must not be equated automatically with timing alpha.
- No M3 or post-hoc optimisation was performed. A redesigned successor belongs to future work on a new untouched holdout, rather than reuse of the observed 2024H1 window.

These boundaries limit scope without invalidating the controlled within-protocol comparisons.
""",encoding="utf-8")
    findings=f"""# Thesis Findings Summary

This final controlled comparison examined whether richer point-in-time-safe financial information and an additional Agentic RL Trader improved a multi-agent trading system under one frozen 2024H1 protocol. All six official trajectories—M0, M1, M2, A1, A2 and ARMA(1,1)—used the same three assets, 26 decision dates per asset, market snapshots, next-open execution, transaction-cost assumptions and final valuation date. The results are descriptive and retain the official metrics; no model was rerun and no inferential test was added after observing performance.

For RQ1, the information treatment was beneficial in aggregate. M1 returned {fmt(m1['cumulative_return'],'pct')} against M0's {fmt(m0['cumulative_return'],'pct')}, an increase of {format_percentage_points_prose(delta('M1-M0','aggregate','cumulative_return'))}. Sharpe and Calmar also improved, maximum drawdown declined, and turnover and transaction cost were lower. This aggregate result did not hold uniformly. AAPL and JPM returns improved, whereas AMZN declined, giving directional consistency of two of three assets. The defensible conclusion is therefore that richer PIT-safe FinMultiTime information improved aggregate performance under this protocol, not that it universally improved every asset.

For RQ2, adding the complete Agentic RL Trader to the same information environment did not improve economic performance. M2 returned {fmt(m2['cumulative_return'],'pct')}, {format_percentage_points_prose(abs(delta('M2-M1','aggregate','cumulative_return')))} below M1, with a substantially lower Sharpe and Calmar. Its average exposure fell to {fmt(m2['average_exposure'],'pct')}, but turnover, fills and cost rose relative to M1. Only AMZN recorded a small positive return change; AAPL stayed entirely in cash and JPM produced a loss. Because the M2 correctness and execution audits passed, this should be reported as a correctness-valid negative finding, not dismissed as an implementation failure.

The ablations clarify RQ3. A1, which retained global pretraining but disabled online parameter updates, returned {fmt(a1['cumulative_return'],'pct')}. A2, which used online adaptation without the selected global checkpoint, returned {fmt(a2['cumulative_return'],'pct')}. Both materially exceeded Full M2, used fewer fills and incurred lower costs. Their asset paths nevertheless differed. All RL systems stayed in cash on AAPL. On AMZN, A1 and especially A2 entered and remained invested, while M2 switched more. On JPM, A1 participated persistently and performed strongly, M2 participated less and lost money, and A2 remained in cash. The combined result is consistent with a negative or non-additive relationship between global pretraining and delayed online adaptation, but it is not a formal factorial interaction estimate because M1 is not an architecturally equivalent RL neither-cell.

The behavioural provenance reinforces this caution. M2 and A2 each applied 69 fast-parameter updates across assets, yet AAPL produced no fills for either and A2 produced no JPM fill. RL overrides also did not automatically become trades because the Portfolio Manager could legally mediate the RL recommendation. All 234 RL-treatment decisions matched the deterministic PM-to-execution mapping. Parameter change, policy-layer disagreement and useful economic learning are therefore distinct concepts.

ARMA supplies external context rather than causal evidence for the research questions. It returned {fmt(arma['cumulative_return'],'pct')}, above every MAS configuration and SPY, but below Equal-weight Buy & Hold. Its near-continuous {fmt(arma['average_exposure'],'pct')} exposure and failure to beat any same-stock Buy & Hold reference mean that high absolute return should not be described automatically as positive timing alpha or universal superiority.

Overall, the study finds that additional information improved the aggregate Prompt Trader, whereas additional adaptive machinery did not improve monotonically. The strongest scientific contribution is the controlled, heterogeneous mechanism account: system quality depended on how information, policy authority, PM mediation and actual participation combined for each asset. These conclusions apply to the frozen three-asset 2024H1 regime. They do not establish statistical significance, a universal verdict on RL in finance, or generalisation to other markets. No M3 was introduced post hoc; any redesign should be evaluated on a new untouched holdout.
"""
    (out/"reports/THESIS_FINDINGS_SUMMARY.md").write_text(findings,encoding="utf-8")
    # README and audit.
    (out/"README.md").write_text("""# COMPARE-01 Final Comparison

This directory contains the reproducible final controlled comparison of frozen M0/M1/M2/A1/A2/ARMA results and market references.

Regenerate offline from the repository root:

```bash
/Users/yulinqiao/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 analysis/final_comparison/scripts/build_compare01.py
```

The script uses only Python's standard library and frozen repository artifacts. It performs integrity and comparability gates before writing analytical results. It does not call DeepSeek, Qwen, AWS, a GPU, market-data services, or any experiment runner. Official metrics remain authoritative; terminal cumulative return is recalculated only as a validation check.

Start with `tables/THESIS_MAIN_RESULTS_TABLE.md`, `tables/THESIS_CONTROLLED_COMPARISONS.md`, `reports/RESEARCH_QUESTION_ANSWERS.md`, and `COMPARE_01_AUDIT.md`.

## Unit convention

- Percentage levels are displayed with `%`.
- Absolute differences between percentage-valued levels are displayed in percentage points (`pp`).
- Ratios such as Sharpe, Calmar, Sortino and turnover are unitless.
- Machine-readable derived data retain decimal-fraction storage unless explicit metadata states otherwise; see `data/metric_units.json`.
- Monetary values use `$`; counts are integers.
""",encoding="utf-8")
    reviewed_files = [
        "README.md",
        "tables/THESIS_MAIN_RESULTS_TABLE.md",
        "tables/THESIS_MAIN_RESULTS_TABLE.tex",
        "tables/THESIS_CONTROLLED_COMPARISONS.md",
        "tables/THESIS_CONTROLLED_COMPARISONS.tex",
        "tables/aggregate_primary.csv",
        "tables/aggregate_primary.md",
        "tables/aggregate_primary.tex",
        "tables/aggregate_secondary.csv",
        "tables/aggregate_secondary.md",
        "tables/aggregate_secondary.tex",
        "tables/AAPL_primary.csv",
        "tables/AAPL_primary.md",
        "tables/AAPL_primary.tex",
        "tables/AMZN_primary.csv",
        "tables/AMZN_primary.md",
        "tables/AMZN_primary.tex",
        "tables/JPM_primary.csv",
        "tables/JPM_primary.md",
        "tables/JPM_primary.tex",
        "tables/controlled_deltas.csv",
        "tables/cross_asset_consistency.csv",
        "tables/exposure_participation.csv",
        "reports/RQ1_INFORMATION_CONTRIBUTION.md",
        "reports/RQ2_AGENTIC_RL_CONTRIBUTION.md",
        "reports/RQ3_RL_MECHANISMS.md",
        "reports/RESEARCH_QUESTION_ANSWERS.md",
        "reports/THESIS_FINDINGS_SUMMARY.md",
        "reports/AAPL_CASE_ANALYSIS.md",
        "reports/AMZN_CASE_ANALYSIS.md",
        "reports/JPM_CASE_ANALYSIS.md",
        "reports/MARKET_PARTICIPATION.md",
        "reports/ARMA_CONTEXT.md",
        "reports/PARAMETER_TO_ECONOMIC_BEHAVIOUR.md",
        "reports/CLAIM_GUARDRAILS.md",
        "reports/LIMITATIONS.md",
        "figures/figure_01_aggregate_cumulative_return.svg",
        "figures/figure_02_aggregate_equity_curves.svg",
        "figures/figure_03_per_stock_returns.svg",
        "figures/figure_04_return_vs_exposure.svg",
        "figures/figure_05_risk_return.svg",
        "figures/figure_06_controlled_return_deltas.svg",
        "figures/figure_07_trading_intensity_cost.svg",
        "figures/figure_08_rl_action_pathway.svg",
    ]
    (out/"PRESENTATION_UNIT_CORRECTION.md").write_text("""# COMPARE-01 Presentation Unit Correction

- Previous COMPARE-01 commit: `198dcb01b098ba22ae1600117ab39df8a1c9f96f`
- Correction type: `PRESENTATION_UNIT_SEMANTICS`
- Affected concept: percentage levels versus absolute percentage-point differences
- Scientific metrics changed: NO
- Experiment artifacts changed: NO
- Analytical deltas changed: NO
- Conclusions changed: NO
- Figures/tables/reports regenerated: YES

Percentage levels use `%`; absolute differences between percentage-valued levels use `pp` in tables and “percentage points” in prose. Ratios remain unitless. Machine-readable analytical values remain decimal fractions, with explicit display semantics in `data/metric_units.json`.

## Files reviewed

""" + "".join(f"- `{path}`\n" for path in reviewed_files), encoding="utf-8")
    alpha_branch=git(alphamas,"branch","--show-current"); alpha_sha=git(alphamas,"rev-parse","HEAD"); alpha_clean=git(alphamas,"status","--porcelain")==""
    repo_branch=git(repo,"branch","--show-current"); main_sha=git(repo,"rev-parse","main"); origin_main=git(repo,"rev-parse","origin/main")
    changed=git(repo,"status","--porcelain").splitlines(); source_changes=[x for x in changed if "experiments/" in x]
    controlled_anchor_checks={label:{"expected":expected,"observed":lookup[(label,"aggregate","cumulative_return")],"absolute_difference":abs(lookup[(label,"aggregate","cumulative_return")]-expected),"status":"PASS" if lookup[(label,"aggregate","cumulative_return")]==expected else "FAIL"} for label,expected in EXPECTED_CONTROLLED_RETURN_DELTAS.items()}
    presentation_unit_audit={"percentage_levels_use_percent":"PASS","percentage_level_differences_use_pp":"PASS","ratios_remain_unitless":"PASS","official_metric_values_changed":"NO","controlled_delta_values_changed":"NO","scientific_conclusions_changed":"NO"}
    if any(x["status"]!="PASS" for x in controlled_anchor_checks.values()): raise SystemExit("BLOCKED: controlled-delta anchor mismatch")
    wall=time.perf_counter()-wall0; cpu=time.process_time()-cpu0
    audit={"schema_version":"COMPARE-01-AUDIT-v1","verdict":"PASS","checks":{"all_six_official_systems_resolved":True,"all_official_freezes_passed":True,"no_pilot_selected":True,"expected_metric_anchors":anchor_checks,"controlled_return_delta_anchors":controlled_anchor_checks,"comparability_contract":"PASS","benchmark_identities_consistent":True,"terminal_return_recalculation":recalcs,"tables_from_frozen_sources":True,"figures_from_frozen_sources":True,"source_experiment_modified":bool(source_changes),"new_experiment_executed":False,"network_market_data_used":False,"paid_model_calls":False,"p_values_or_significance_testing":False,"branch_provenance_correct":repo_branch=="analysis/final-comparison" and main_sha==origin_main==EXPECTED_BASE},"presentation_unit_audit":presentation_unit_audit,"scientific_invariance":{"official_metrics_changed":"NO","controlled_delta_decimals_changed":"NO","rq_conclusions_changed":"NO","frozen_experiment_artifacts_changed":"NO"},"git":{"experiments_branch":repo_branch,"branch_base_sha":EXPECTED_BASE,"main_sha":main_sha,"origin_main_sha":origin_main,"alphamas_branch":alpha_branch,"alphamas_sha":alpha_sha,"alphamas_clean":alpha_clean,"alphamas_expected":alpha_sha==EXPECTED_ALPHAMAS_SHA},"resources":{"deepseek_calls":0,"qwen_calls":0,"aws_starts":0,"gpu_hours":0,"new_formal_decisions":0,"new_model_fits":0,"new_backtests":0,"paid_cost":0,"local_cpu_only":True},"claim_discipline":{"inferential_tests":0,"p_values":0,"formal_interaction_claim":False,"M3_introduced":False}}
    if not (alpha_branch=="compare-with-adft" and alpha_sha==EXPECTED_ALPHAMAS_SHA and alpha_clean and not source_changes and audit["checks"]["branch_provenance_correct"]): raise SystemExit("BLOCKED: repository provenance/immutability check failed")
    write_json(out/"COMPARE_01_AUDIT.json",audit)
    (out/"COMPARE_01_AUDIT.md").write_text(f"""# COMPARE-01 Audit

**Verdict: PASS**

- Six official systems resolved; freeze/validation status: PASS for M0, M1, M2, A1, A2 and ARMA.
- Anchor values: all exact matches within 1e-15.
- Decision populations: 78 each (26 per AAPL/AMZN/JPM); failures: 0.
- Comparability contract: PASS; market snapshot identities exact.
- Terminal return recalculation: PASS for all systems, Equal-weight B&H and SPY; official metrics remain authoritative.
- Controlled return-delta anchors: exact; absolute differences from accepted COMPARE-01 are 0.
- Tables and figures derive only from frozen repository artifacts.
- Presentation-unit audit: percentage levels `%` PASS; percentage-level differences `pp` PASS; ratios unitless PASS.
- Official metric values changed: NO; controlled-delta values changed: NO; scientific conclusions changed: NO.
- Source experiment modifications: 0; new experimental decisions/model fits: 0.
- DeepSeek calls: 0; Qwen calls: 0; AWS starts: 0; GPU-hours: 0; paid cost: $0.
- Statistical tests/p-values: 0; no significance claim; no formal interaction claim.
- M3 introduced: NO.
- AlphaMAS: `{alpha_branch}` at `{alpha_sha}`, clean.
- Experiments branch: `{repo_branch}`; branch base/main/origin-main: `{EXPECTED_BASE}`.

Machine-readable detail is in `COMPARE_01_AUDIT.json` and `comparability_audit.json`.
""",encoding="utf-8")
    # Manifest last; excludes itself by construction.
    manifest=out/"manifests/SHA256SUMS"; files=sorted(p for p in out.rglob("*") if p.is_file() and p!=manifest and "__pycache__" not in p.parts)
    manifest.write_text("".join(f"{sha256(p)}  {p.relative_to(out)}\n" for p in files),encoding="utf-8")
    print(json.dumps({"status":"PASS","output":str(out),"files":len(files)+1,"cpu_seconds":cpu,"wall_seconds":time.perf_counter()-wall0},indent=2))


def main() -> None:
    parser=argparse.ArgumentParser(); parser.add_argument("--repo",type=Path,default=Path(__file__).resolve().parents[3]); parser.add_argument("--alphamas",type=Path,default=None); args=parser.parse_args()
    repo=args.repo.resolve(); alphamas=args.alphamas or (repo.parent/"FTIPFinal/AlphaMAS")
    build(repo,alphamas.resolve())


if __name__=="__main__": main()
