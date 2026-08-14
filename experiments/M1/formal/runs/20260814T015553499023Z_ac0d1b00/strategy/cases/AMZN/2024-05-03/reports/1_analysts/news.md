All data sources are returning `DATA_UNAVAILABLE_IN_HISTORICAL_MODE`. Let me compile my report based on what's available and clearly state what is unavailable.

---

# AMZN News & Macro Research Report
**Analysis Date:** 2024-05-03 (Historical Run)
**Instrument:** `AMZN`

## Executive Summary

This report was tasked with analyzing recent news and macroeconomic trends relevant to trading `AMZN` as of **2024-05-03**. However, **all data sources returned `DATA_UNAVAILABLE_IN_HISTORICAL_MODE`** for the requested historical window. I must transparently report this rather than fill gaps with unverified information.

## Data Availability Status

| Data Source | Tool Used | Status |
|---|---|---|
| Company-specific news (`AMZN`) | `get_news` | **UNAVAILABLE** — No timestamped articles in archive for 2024-04-26 to 2024-05-03 (or extended 2024-04-01 to 2024-05-03 window) |
| Global macro news | `get_global_news` | **UNAVAILABLE** — No timestamped articles in archive for the 7-day or 30-day lookback |
| Fed Funds Rate | `get_macro_indicators` | **UNAVAILABLE** — FRED is a LIVE_ONLY source, disabled in historical mode |
| CPI | `get_macro_indicators` | **UNAVAILABLE** — FRED is a LIVE_ONLY source, disabled in historical mode |
| Unemployment | `get_macro_indicators` | **UNAVAILABLE** — FRED is a LIVE_ONLY source, disabled in historical mode |
| 10Y Treasury | `get_macro_indicators` | **UNAVAILABLE** — FRED is a LIVE_ONLY source, disabled in historical mode |
| Fed rate cut prediction markets | `get_prediction_markets` | **UNAVAILABLE** — Polymarket is a LIVE_ONLY source, disabled in historical mode |
| Recession prediction markets | `get_prediction_markets` | **UNAVAILABLE** — Polymarket is a LIVE_ONLY source, disabled in historical mode |

## Analysis

### 1. Company-Specific News (`AMZN`)
**Status: UNAVAILABLE.** The Yahoo Finance news archive returned no timestamped articles for `AMZN` within the strict historical window (2024-04-26 to 2024-05-03), nor for the extended window (2024-04-01 to 2024-05-03). Archive completeness is not guaranteed in historical mode. I cannot report on earnings, product launches, AWS developments, or any company-specific catalysts for `AMZN` during this period.

### 2. Global Macro News
**Status: UNAVAILABLE.** No global macroeconomic news articles were available for the 7-day or 30-day lookback windows ending 2024-05-03.

### 3. Macroeconomic Indicators (FRED)
**Status: UNAVAILABLE.** The FRED data source is a LIVE_ONLY source and was disabled before its network request in historical mode. I cannot report on:
- Fed Funds Rate
- CPI / inflation
- Unemployment
- 10-Year Treasury yields
- Yield curve positioning

### 4. Prediction Markets (Polymarket)
**Status: UNAVAILABLE.** Polymarket is a LIVE_ONLY source and was disabled in historical mode. I cannot report on market-implied probabilities for:
- Fed rate cut timing
- Recession risk within the next 12 months
- Any other forward-looking events

## Key Takeaways

1. **No actionable evidence could be retrieved** for `AMZN` for the analysis date of 2024-05-03 due to the historical-mode restrictions on all data sources.
2. **I will not fabricate or infer** news, macro data, or market probabilities that are not supported by the available evidence.
3. **Recommendation:** Given the complete absence of verifiable evidence, I cannot provide a data-driven BUY/HOLD/SELL recommendation for `AMZN` at this time. Any recommendation would be speculative and not grounded in the supplied evidence.

## Summary Table

| Category | Source | Availability | Key Findings |
|---|---|---|---|
| `AMZN` Company News | Yahoo Finance | ❌ UNAVAILABLE | No timestamped articles in historical window |
| Global Macro News | Yahoo Finance | ❌ UNAVAILABLE | No articles available for lookback window |
| Fed Funds Rate | FRED | ❌ UNAVAILABLE | LIVE_ONLY source disabled in historical mode |
| CPI | FRED | ❌ UNAVAILABLE | LIVE_ONLY source disabled in historical mode |
| Unemployment | FRED | ❌ UNAVAILABLE | LIVE_ONLY source disabled in historical mode |
| 10Y Treasury | FRED | ❌ UNAVAILABLE | LIVE_ONLY source disabled in historical mode |
| Fed Rate Cut Markets | Polymarket | ❌ UNAVAILABLE | LIVE_ONLY source disabled in historical mode |
| Recession Markets | Polymarket | ❌ UNAVAILABLE | LIVE_ONLY source disabled in historical mode |

---

**Bottom Line:** This is a data-availability-limited report. All evidence sources were unavailable for the historical analysis date of 2024-05-03. No trading recommendation can be responsibly issued for `AMZN` based on the supplied evidence. I recommend re-running this analysis with a live data connection or with a historical window for which archived data exists.

FINAL TRANSACTION PROPOSAL: **HOLD** (no actionable evidence to support a BUY or SELL; holding is the neutral default given data unavailability)