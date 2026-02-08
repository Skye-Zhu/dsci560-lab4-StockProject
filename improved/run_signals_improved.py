from pathlib import Path
import pandas as pd
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT / "src"))

from loader import load_prices  # noqa: E402
from strategy_improved import signals_sma_band_cooldown  # noqa: E402


def main():
    data_path = ROOT / "data" / "prices_15m.csv"
    out_dir = ROOT / "outputs"
    out_dir.mkdir(exist_ok=True)

    df = load_prices(str(data_path))
    symbol = df["symbol"].iloc[0]
    d1 = df[df["symbol"] == symbol].copy().sort_values("timestamp").reset_index(drop=True)

    sig = signals_sma_band_cooldown(
        d1,
        short_w=10,
        long_w=30,
        band=0.003,          #  0.003
        cooldown_bars=12     #also try 24
    )

    out_path = out_dir / f"signals_{symbol}_improved_15m.csv"
    sig.to_csv(out_path, index=False)

    print(f"Saved improved signals to: {out_path}")
    print("Signal counts:")
    print(sig["signal"].value_counts())


if __name__ == "__main__":
    main()