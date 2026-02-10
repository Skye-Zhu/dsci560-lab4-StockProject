from pathlib import Path
import pandas as pd

from loader import load_prices
from strategy import sma_crossover_signals

def main():
    root = Path(__file__).resolve().parents[1]
    data_path = root / "data" / "prices.csv"
    out_dir = root / "outputs"
    out_dir.mkdir(exist_ok=True)

    df = load_prices(str(data_path))


    symbol = df["symbol"].iloc[0]
    d1 = df[df["symbol"] == symbol].copy()

    d1 = d1.sort_values("timestamp").reset_index(drop=True)

    sig = sma_crossover_signals(d1, short_w=10, long_w=30)

    out_path = out_dir / f"signals_{symbol}.csv"
    sig.to_csv(out_path, index=False)

    print(f"Saved signals to: {out_path}")
    print("Last 12 rows preview:")
    print(sig.tail(12)[["timestamp", "symbol", "price", "sma_short", "sma_long", "position", "signal"]])


    print("\nSignal counts:")
    print(sig["signal"].value_counts())

if __name__ == "__main__":
    main()