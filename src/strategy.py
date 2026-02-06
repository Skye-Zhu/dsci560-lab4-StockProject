import pandas as pd
from indicators import sma

def sma_crossover_signals(
    df: pd.DataFrame,
    short_w: int = 10,
    long_w: int = 30,
    price_col: str = "price"
) -> pd.DataFrame:
    if short_w >= long_w:
        raise ValueError("short_w must be smaller than long_w")

    out = df.copy()
    out["sma_short"] = sma(out[price_col], short_w)
    out["sma_long"]  = sma(out[price_col], long_w)

    # position：1=持仓，0=空仓
    out["position"] = (out["sma_short"] > out["sma_long"]).astype(int)

    # trade
    # +1 表示BUY，-1 表示从SELL
    out["trade"] = out["position"].diff()

    out["signal"] = "HOLD"
    out.loc[out["trade"] == 1, "signal"] = "BUY"
    out.loc[out["trade"] == -1, "signal"] = "SELL"

    return out