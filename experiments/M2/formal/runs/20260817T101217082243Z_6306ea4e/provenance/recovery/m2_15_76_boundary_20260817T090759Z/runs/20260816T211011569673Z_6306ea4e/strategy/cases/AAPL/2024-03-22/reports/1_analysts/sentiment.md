**Overall Sentiment:** **Neutral** (Score: 5.0/10)
**Confidence:** Low

## AAPL Sentiment Report — 2024-03-15 to 2024-03-22

### Data Availability Statement

**Critical caveat up front:** All three intended data sources returned placeholders for this historical window. This is a historical-mode run with `historical_as_of=2024-03-22T20:00:00+00:00`, and the pre-fetched sources were disabled or incomplete for that period:

- **Yahoo Finance news:** `DATA_UNAVAILABLE_IN_HISTORICAL_MODE` — no timestamped articles remained after the strict historical window/as_of filter; archive completeness is not guaranteed.
- **StockTwits:** `DATA_UNAVAILABLE_IN_HISTORICAL_MODE` — live-only source, disabled for historical analysis.
- **Reddit (r/wallstreetbets, r/stocks, r/investing):** `DATA_UNAVAILABLE_IN_HISTORICAL_MODE` — live-only source, disabled for historical analysis.

Because no substantive sentiment data points were supplied, I cannot compute a Bullish/Bearish ratio, engagement-weighted Reddit signals, or cross-source divergences. I will not fabricate or infer sentiment from events outside the supplied evidence.

---

### 1. Source-by-Source Breakdown

**Yahoo Finance news (institutional framing):** Unavailable. No headlines were provided for the 2024-03-15 to 2024-03-22 window. No institutional narrative can be assessed.

**StockTwits (retail sentiment):** Unavailable. No messages, no Bullish/Bearish ratio, no sample size. Retail sentiment cannot be measured.

**Reddit (community discussion):** Unavailable across all three target subreddits (r/wallstreetbets, r/stocks, r/investing). No posts, upvote scores, or comment counts were provided. Community engagement cannot be measured.

---

### 2. Cross-Source Divergences and Alignments

No divergences or alignments can be identified because no source returned data. There is no signal to compare across sources.

---

### 3. Dominant Narrative Themes

No narrative themes can be extracted from the supplied evidence. The data is silent on AAPL for this window.

---

### 4. Catalysts and Risks

No catalysts or risks were surfaced by the data. I will not speculate on events occurring after `historical_as_of` or outside the supplied evidence. Any trader relying on this report should note that sentiment inputs are entirely absent for the window.

---

### 5. Key Sentiment Signals Summary

| Direction | Source | Supporting Evidence |
|-----------|--------|--------------------|
| — (no signal) | Yahoo Finance news | Data unavailable in historical mode |
| — (no signal) | StockTwits | Data unavailable in historical mode |
| — (no signal) | Reddit (all subreddits) | Data unavailable in historical mode |

---

### Overall Assessment

**overall_band: Neutral** — This reflects genuine silence across all sources, not a balanced bullish/bearish mix. Per the rubric, Neutral is appropriate only when all sources are genuinely silent, which is exactly the case here.

**overall_score: 5.0** — Neutral midpoint, consistent with the absence of any directional signal.

**confidence: low** — Confidence is low because all three sources returned placeholders and no substantive data points exist. This report should be treated as a data-availability flag rather than a sentiment read.

**Recommendation to downstream consumers:** Do not treat this as a directional sentiment signal for AAPL. The sentiment layer is effectively empty for the 2024-03-15 to 2024-03-22 window. Any trading decision must rely on fundamentals, technicals, and other data layers, since the sentiment dimension provides no usable evidence here.