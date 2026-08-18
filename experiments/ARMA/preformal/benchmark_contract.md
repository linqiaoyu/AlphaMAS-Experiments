# ARMA11 pre-Formal benchmark contract

The fixed `ARMA11_FIXED_V1` method was frozen before any 2024H1 ARMA trading
performance was computed or inspected.

- Methodology source SHA (`ARMA_PREFORMAL_SOURCE_SHA`): `d33bf08a90f9cb5bb6f4511e66fda8babd9d65e0`
- Freeze-record source SHA: `c4592b915ea3e08760b0142b738e560139e32456`
- Frozen Full-M2 parent: `6306ea4ea20cda501c6238db80c34d27bbc16bea`
- Config SHA256: `fa193e253716faeb4a3235c0a1ff51dc9f75f95bf01564153ccec7a3e5eb1fc5`
- Model: `statsmodels.tsa.arima.model.ARIMA(order=(1,0,1), trend="c", enforce_stationarity=True, enforce_invertibility=True)`
- Fit: `method="statespace"`, `maxiter=200`
- Input: exactly 252 daily simple PIT total returns from 253 consecutive raw-price/action observations
- Horizon: exactly five daily forecasts, compounded as `prod(1+r_hat)-1`
- Signal: positive to 100% long; zero or negative to cash
- Hard failure: HOLD and preserve the current discrete position; no retry
- PIT structural audit: 78/78 exact windows, zero future violations, zero insufficient windows
- Performance-based tuning: none
- Paid/agent compute: none
