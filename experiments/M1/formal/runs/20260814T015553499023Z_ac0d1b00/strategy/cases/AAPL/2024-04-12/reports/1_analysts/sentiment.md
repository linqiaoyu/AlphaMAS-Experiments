**Overall Sentiment:** **Neutral** (Score: 5.0/10)
**Confidence:** Low

## AAPL Sentiment Report — 2024-04-05 to 2024-04-12

### Data Availability & Source-by-Source Breakdown

**Important caveat up front:** This is a historical run with `historical_as_of=2024-04-12T20:00:00+00:00`. All three pre-fetched data sources returned placeholders indicating that the underlying data is **unavailable in historical mode**. This severely limits the robustness of any sentiment read.

1. **Yahoo Finance news headlines** — `DATA_UNAVAILABLE_IN_HISTORICAL_MODE`. The archive is incomplete for the requested window (2024-04-05 to 2024-04-12), and no timestamped articles survived the strict historical window/as_of filter. **No institutional news framing is available.**

2. **StockTwits messages** — `DATA_UNAVAILABLE_IN_HISTORICAL_MODE`. StockTwits is a live-only source and was disabled for historical analysis. **No retail Bullish/Bearish ratio or message counts are available.**

3. **Reddit posts (r/wallstreetbets, r/stocks, r/investing)** — `DATA_UNAVAILABLE_IN_HISTORICAL_MODE`. Reddit is a live-only source and was disabled for historical analysis. **No community engagement data (upvotes, comment counts, post bodies) is available.**

### Cross-Source Divergences

None can be assessed. With all three sources returning unavailable placeholders, there is no data to compare across sources, and therefore no divergence or alignment signal can be identified. The typical cross-source checks (news-vs-retail divergence, engagement-weighted Reddit themes) cannot be performed.

### Dominant Narrative Themes

No narrative themes can be extracted from the supplied evidence because no message bodies, headlines, or post excerpts were provided. I will not fabricate or infer themes (e.g., no assumptions about AAPL earnings, product cycles, or macro headlines) since doing so would rely on facts or events outside the supplied evidence and potentially after the historical cutoff.

### Catalysts and Risks

No catalysts or risks can be surfaced from the supplied data. Any mention of upcoming earnings, product launches, or competitive threats would be speculative and unsupported by the evidence provided. I explicitly flag that no catalyst/risk information is available in this window.

### Key Sentiment Signals Summary

| Direction | Source | Supporting Evidence |
|-----------|--------|--------------------|
| N/A (no signal) | Yahoo Finance news | Data unavailable in historical mode; no timestamped articles in window |
| N/A (no signal) | StockTwits | Live-only source disabled for historical analysis; no messages |
| N/A (no signal) | Reddit (WSB/stocks/investing) | Live-only source disabled for historical analysis; no posts |

### Overall Assessment

Because every source returned an unavailable placeholder, there is **no substantive sentiment signal** for AAPL in this window. Per the guidance, `Neutral` is appropriate only when all sources are genuinely silent — which is exactly the case here. This is a data-availability outcome, not a genuine market-neutral read. The `overall_score` of 5.0 reflects the absence of any directional evidence rather than a balanced mix of bullish and bearish inputs.

**Confidence: low.** With zero data points across all three sources, the sentiment read is not robust. I recommend the trader treat this as a "no-signal" situation and rely on fundamentals and technicals, or re-run the analysis with live data sources enabled. Past sentiment is not predictive, and here there is no past sentiment to weigh at all.