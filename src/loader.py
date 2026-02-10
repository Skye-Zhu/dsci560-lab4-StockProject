import pandas as pd

def load_prices(
    csv_path: str,
    ts_col: str = "timestamp",
    symbol_col: str = "symbol",
    price_col: str = "price"
) -> pd.DataFrame:

    df = pd.read_csv(csv_path)

    df = df.rename(columns={
        ts_col: "timestamp",
        symbol_col: "symbol",
        price_col: "price"
    })

    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df = df.sort_values(["symbol", "timestamp"]).reset_index(drop=True)


    df = df.dropna(subset=["timestamp", "symbol", "price"])
    df = df[df["price"] > 0]

    return df