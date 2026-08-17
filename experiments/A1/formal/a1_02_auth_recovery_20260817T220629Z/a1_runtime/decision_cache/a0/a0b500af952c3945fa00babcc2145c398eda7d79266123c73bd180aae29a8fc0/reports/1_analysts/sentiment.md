**Overall Sentiment:** **Neutral** (Score: 5.0/10)
**Confidence:** Low

## AMZN Sentiment Report — 2024-05-24 to 2024-05-31

### Data Availability Statement (Critical)

**All three designated sentiment sources returned placeholders for the requested historical window.** This is a historical-mode run with `historical_as_of=2024-05-31T20:00:00+00:00`, and the data pipeline reported the following:

- **Yahoo Finance news**: `DATA_UNAVAILABLE_IN_HISTORICAL_MODE` — the archive is incomplete for the window 2024-05-24 to 2024-05-31; no timestamped articles survived the strict historical window/as_of filter; archive completeness is not guaranteed.
- **StockTwits**: `DATA_UNAVAILABLE_IN_HISTORICAL_MODE` — StockTwits is a live-only source and was disabled for historical analysis.
- **Reddit (r/wallstreetbets, r/stocks, r/investing)**: `DATA_UNAVAILABLE_IN_HISTORICAL_MODE` — Reddit is a live-only source and was disabled for historical analysis.

### Source-by-Source Breakdown

**1. News headlines (Yahoo Finance):** No data available. No institutional-framing headlines, no event-driven news, no analyst commentary could be retrieved for the window. Cannot assess institutional sentiment, catalysts, or risk framing.

**2. StockTwits messages:** No data available. No retail Bullish/Bearish ratio, no message counts, no retail narrative themes could be retrieved. The leading retail-sentiment signal is entirely absent.

**3. Reddit posts:** No data available. No engagement-weighted threads, no upvote/comment counts, no community discussion across any of the three target subreddits could be retrieved.

### Cross-Source Divergences

Not assessable — there is no data from any source with which to compare or contrast. No divergence or alignment signals can be identified.

### Dominant Narrative Themes

None identifiable. With all three sources silent, there is no recurring theme, no dominant narrative, and no sentiment signal to extract.

### Catalysts and Risks

None surfaced by the data. No earnings, product-launch, competitive, or macro catalysts/risks could be identified from the supplied evidence. (Note: I am not filling this gap with post-hoc knowledge; per instructions, unavailable evidence is stated as unavailable.)

### Key Sentiment Signals Summary

| Direction | Source | Supporting Evidence |
|-----------|--------|---------------------|
| N/A | Yahoo Finance news | Data unavailable in historical mode |
| N/A | StockTwits | Data unavailable (live-only source) |
| N/A | Reddit (WSB/stocks/investing) | Data unavailable (live-only source) |

### Conclusion

Because every source returned a placeholder, the sentiment read is **not robust** and carries **low confidence**. The `overall_band` is set to **Neutral** and `overall_score` to **5.0** strictly because all sources are genuinely silent — this reflects an absence of evidence, not a genuine neutral market posture. This should be treated as a **data-gap flag**, not a sentiment signal.

**Recommendation to downstream consumers:** Do not treat this as a directional read on AMZN. The trader should rely on fundamentals and technicals for this window, and sentiment should be re-collected from live sources (or a more complete news archive) before any sentiment-weighted decision is made. No BUY/HOLD/SELL signal is derivable from the supplied evidence.