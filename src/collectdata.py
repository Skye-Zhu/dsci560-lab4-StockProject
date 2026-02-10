import yfinance as yf
import pandas as pd
from pathlib import Path

def collect_stock_data(
    ticker="AAPL",
    period="1mo",
    interval="5m"
):
    stock = yf.Ticker(ticker)
    df = stock.history(period=period, interval=interval)

    if df.empty:
        raise ValueError("No data fetched. Check ticker or interval.")

    df = df.reset_index()


    df = df.rename(columns={
        "Datetime": "timestamp",
        "Date": "timestamp",
        "Close": "price"
    })

    df["symbol"] = ticker
    df = df[["timestamp", "symbol", "price"]]

    return df


if __name__ == "__main__":
    root = Path(__file__).resolve().parents[1]
    data_dir = root / "data"
    data_dir.mkdir(exist_ok=True)

    df = collect_stock_data(
        ticker="AAPL",
        period="1mo",
        interval="5m"
    )

    out_path = data_dir / "prices.csv"
    df.to_csv(out_path, index=False)

    print(f"Saved {len(df)} rows to {out_path}")
    print(df.head())