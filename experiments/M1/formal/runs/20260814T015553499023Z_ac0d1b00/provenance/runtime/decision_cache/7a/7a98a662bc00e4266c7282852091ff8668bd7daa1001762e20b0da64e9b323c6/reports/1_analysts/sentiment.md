**Overall Sentiment:** **Neutral** (Score: 5.0/10)
**Confidence:** Low

## AMZN Sentiment Report — 2024-04-19 to 2024-04-26

### Data Availability & Source-by-Source Breakdown

**Important caveat up front:** This is a historical-mode analysis with `historical_as_of=2024-04-26T20:00:00+00:00`. All three intended data sources returned placeholders indicating data unavailability for the requested window. This materially limits the robustness of any sentiment read.

**1. News headlines (Yahoo Finance):** `DATA_UNAVAILABLE_IN_HISTORICAL_MODE`. The Yahoo Finance archive is incomplete for the 2024-04-19 to 2024-04-26 window; no timestamped articles survived the strict historical window/as_of filter. No institutional news framing is available. This removes the slow-moving, fact-driven signal entirely.

**2. StockTwits messages:** `DATA_UNAVAILABLE_IN_HISTORICAL_MODE`. StockTwits is a live-only source and was disabled for historical analysis. No retail Bullish/Bearish ratio, message counts, or sentiment tags are available. This removes the fast-moving retail signal entirely.

**3. Reddit posts (r/wallstreetbets, r/stocks, r/investing):** `DATA_UNAVAILABLE_IN_HISTORICAL_MODE`. Reddit is a live-only source and was disabled for historical analysis. No community discussion, upvote scores, comment counts, or post bodies are available. This removes the engagement-weighted community signal entirely.

### Cross-Source Divergences & Alignments

No divergences or alignments can be assessed because no source returned substantive data. There is no basis to compare institutional framing against retail sentiment or community engagement.

### Dominant Narrative Themes

None can be identified from the supplied evidence. There is no recurring topic, headline, or discussion thread to extract a dominant narrative from. I will not fabricate themes, catalysts, or risks in the absence of data.

### Catalysts & Risks

No catalysts or risks can be surfaced from the supplied evidence. I will not speculate about upcoming earnings, product launches, or macro events, as doing so would rely on facts or events outside the supplied data and potentially after the historical_as_of cutoff.

### Key Sentiment Signals Summary

| Direction | Source | Supporting Evidence |
|-----------|--------|---------------------|
| N/A | Yahoo Finance news | Data unavailable in historical mode; no timestamped articles in window |
| N/A | StockTwits | Data unavailable in historical mode; live-only source disabled |
| N/A | Reddit (WSB/stocks/investing) | Data unavailable in historical mode; live-only source disabled |

### Conclusion

Because all three sources returned placeholders, the sentiment read is **not robust**. Per the analysis guidelines, when all sources are genuinely silent, the appropriate band is **Neutral** with a neutral score of **5.0**. Confidence is **low** given the complete absence of data. This should be treated as a data-availability flag rather than a genuine signal about AMZN sentiment. The trader should weigh this alongside fundamentals and technicals, and should not interpret the Neutral band as a price call — it reflects an absence of evidence, not evidence of neutrality in the market.