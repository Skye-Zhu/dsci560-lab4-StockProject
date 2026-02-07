import yfinance as yf
from pathlib import Path

def main():
    ticker = "AAPL"
    period = "1mo"
    interval = "15m"

    df = yf.Ticker(ticker).history(period=period, interval=interval)
    df = df.reset_index()

    df = df.rename(columns={
        "Datetime": "timestamp",
        "Date": "timestamp",
        "Close": "price"
    })

    df["symbol"] = ticker
    df = df[["timestamp", "symbol", "price"]]

    root = Path(__file__).resolve().parents[1]
    data_dir = root / "data"
    data_dir.mkdir(exist_ok=True)

    out_path = data_dir / "prices_15m.csv"
    df.to_csv(out_path, index=False)
    print(f"Saved {len(df)} rows to {out_path}")

if __name__ == "__main__":
    main()