from pathlib import Path
import os

from loader import load_prices
from arima_model import arima_forecast


def main():

    root = Path(__file__).resolve().parents[1]
    data_path = root / "data" / "prices.csv"
    output_dir = root / "outputs"
    os.makedirs(output_dir, exist_ok=True)

    df = load_prices(str(data_path))
    price_series = df["price"]


    pred_df, mae, rmse = arima_forecast(price_series)

    output_file = output_dir / "arima_predictions.csv"
    pred_df.to_csv(output_file, index=False)

    print("ARIMA Evaluation Metrics")
    print(f"MAE : {mae:.4f}")
    print(f"RMSE: {rmse:.4f}")
    print(f"Saved ARIMA predictions to: {output_file}")

    print(pred_df["expected_ret"].describe())


if __name__ == "__main__":
    main()
