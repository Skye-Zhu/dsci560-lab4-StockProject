import numpy as np
import pandas as pd

def compute_returns(equity: pd.Series) -> pd.Series:
    return equity.pct_change().dropna()

def annualized_return(equity: pd.Series, periods_per_year: int) -> float:
    r = compute_returns(equity)
    if len(r) == 0:
        return 0.0
    total = equity.iloc[-1] / equity.iloc[0]
    years = len(r) / periods_per_year
    return total ** (1 / years) - 1

def sharpe_ratio(equity: pd.Series, periods_per_year: int, risk_free_rate: float = 0.0) -> float:
    r = compute_returns(equity)
    if len(r) == 0:
        return 0.0

    rf_per_period = (1 + risk_free_rate) ** (1 / periods_per_year) - 1
    excess = r - rf_per_period

    std = excess.std()
    if std == 0 or np.isnan(std):
        return 0.0

    return (excess.mean() / std) * np.sqrt(periods_per_year)