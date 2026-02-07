from pathlib import Path
import pandas as pd

from loader import load_prices
from strategy_band import sma_crossover_signals_with_band

def main():
    root = Path(__file__).resolve().parents[1]
    data_path = root / "data" / "prices.csv"
    out_dir = root / "outputs"
    out_dir.mkdir(exist_ok=True)

    df = load_prices(str(data_path))
    symbol = df["symbol"].iloc[0]
    d1 = df[df["symbol"] == symbol].copy().sort_values("timestamp").reset_index(drop=True)

    sig = sma_crossover_signals_with_band(d1, short_w=10, long_w=30, band=0.001)

    out_path = out_dir / f"signals_{symbol}_band.csv"
    sig.to_csv(out_path, index=False)

    print(f"Saved band signals to: {out_path}")
    print("Signal counts:")
    print(sig["signal"].value_counts())

if __name__ == "__main__":
    main() 