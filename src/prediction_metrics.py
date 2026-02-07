from pathlib import Path
import pandas as pd
import numpy as np

def mae(y_true, y_pred):
    return np.mean(np.abs(y_true - y_pred))

def rmse(y_true, y_pred):
    return np.sqrt(np.mean((y_true - y_pred) ** 2))

def main():
    root = Path(__file__).resolve().parents[1]
    data_path = root / "data" / "prices.csv"
    out_path = root / "outputs" / "prediction_metrics.txt"

    df = pd.read_csv(data_path)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df = df.sort_values("timestamp").reset_index(drop=True)

    # one-step-ahead naive prediction: pred(t+1) = price(t)
    y_true = df["price"].iloc[1:].to_numpy()
    y_pred = df["price"].iloc[:-1].to_numpy()

    m = mae(y_true, y_pred)
    r = rmse(y_true, y_pred)

    with open(out_path, "w") as f:
        f.write("One-step-ahead naive prediction: pred(t+1) = price(t)\n")
        f.write(f"MAE:  {m:.6f}\n")
        f.write(f"RMSE: {r:.6f}\n")

    print(open(out_path).read())
    print(f"Saved to: {out_path}")

if __name__ == "__main__":
    main()