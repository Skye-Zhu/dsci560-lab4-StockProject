import pandas as pd
from pathlib import Path
import sys

SRC_DIR = Path(__file__).resolve().parents[1] / "src"
sys.path.append(str(SRC_DIR))

from indicators import sma  # noqa: E402


def signals_sma_band_cooldown(
    df: pd.DataFrame,
    short_w: int = 10,
    long_w: int = 30,
    band: float = 0.003,         # 0.3%
    cooldown_bars: int = 12,     # 12根5min=60分钟
    price_col: str = "price"
) -> pd.DataFrame:

    if short_w >= long_w:
        raise ValueError("short_w must be smaller than long_w")
    if cooldown_bars < 0:
        raise ValueError("cooldown_bars must be >= 0")

    out = df.copy()

    out["sma_short"] = sma(out[price_col], short_w)
    out["sma_long"] = sma(out[price_col], long_w)

    # 趋势强度（相对差）
    out["band_ratio"] = (out["sma_short"] - out["sma_long"]) / out["sma_long"]

    # 先生成“理想 position”（不考虑 cooldown）
    desired_pos = (out["band_ratio"] > band).astype(int)

    # cooldown 机制：用状态机生成最终 position / signal
    position = []
    signal = []

    pos = 0  # 当前持仓：0空仓，1持仓
    cd = 0   # cooldown 倒计时

    for i in range(len(out)):
        if cd > 0:
            cd -= 1

        
        sig = "HOLD"

        if cd == 0:
            want = int(desired_pos.iloc[i])
            if want == 1 and pos == 0:
                pos = 1
                sig = "BUY"
                cd = cooldown_bars  
            elif want == 0 and pos == 1:
                pos = 0
                sig = "SELL"
                cd = cooldown_bars

        position.append(pos)
        signal.append(sig)

    out["position"] = position
    out["signal"] = signal

    return out