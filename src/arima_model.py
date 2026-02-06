from pathlib import Path
import pandas as pd

from statsmodels.tsa.arima.model import ARIMA
from sklearn.metrics import mean_absolute_error, mean_squared_error

from loader import load_prices


def arima_forecast(
    prices: pd.Series,
    order=(5, 1, 0),
    train_ratio=0.8,
    threshold=0.0,
):
    """
    ARIMA walk-forward forecast + trading signals
    """

    split_idx = int(len(prices) * train_ratio)
    train, test = prices.iloc[:split_idx], prices.iloc[split_idx:]

    history = train.tolist()
    predictions = []

    # ===============================
    # ARIMA rolling forecast
    # ===============================
    for t in range(len(test)):
        model = ARIMA(history, order=order)
        model_fit = model.fit()
        yhat = model_fit.forecast()[0]

        predictions.append(yhat)
        history.append(test.iloc[t])

    # ===============================
    # Evaluation metrics
    # ===============================
    mae = mean_absolute_error(test, predictions)
    rmse = mean_squared_error(test, predictions) ** 0.5

    result = pd.DataFrame(
        {
            "actual": test.values,
            "predicted": predictions,
        },
        index=test.index,
    )

    # ===============================
    # Expected return (no look-ahead)
    # ===============================
    result["expected_ret"] = (
        result["predicted"] - result["actual"].shift(1)
    ) / result["actual"].shift(1)

    # ===============================
    # Signals
    # ===============================
    result["signal"] = "HOLD"
    result.loc[result["expected_ret"] > threshold, "signal"] = "BUY"
    result.loc[result["expected_ret"] < -threshold, "signal"] = "SELL"

    # ===============================
    # Position (state)
    # ===============================
    result["position"] = 0
    for i in range(1, len(result)):
        if result.iloc[i]["signal"] == "BUY":
            result.iloc[i, result.columns.get_loc("position")] = 1
        elif result.iloc[i]["signal"] == "SELL":
            result.iloc[i, result.columns.get_loc("position")] = 0
        else:
            result.iloc[i, result.columns.get_loc("position")] = (
                result.iloc[i - 1]["position"]
            )

    return result, mae, rmse


# =====================================================
# Script entry point
# =====================================================

if __name__ == "__main__":

    # ===============================
    # Project paths
    # ===============================
    ROOT = Path(__file__).resolve().parents[1]
    data_path = ROOT / "data" / "prices.csv"
    out_dir = ROOT / "outputs"
    out_dir.mkdir(exist_ok=True)

    # ===============================
    # Load data
    # ===============================
    df = load_prices(str(data_path))

    # 目前只处理一个 symbol
    symbol = df["symbol"].iloc[0]
    df = df[df["symbol"] == symbol].copy()

    # 确保时间升序
    df = df.sort_values("timestamp").reset_index(drop=True)

    prices = df["price"]

    # ==================================================
    # 1️⃣ First run: threshold = 0 (inspect distribution)
    # ==================================================
    res, mae, rmse = arima_forecast(
        prices=prices,
        threshold=0.0,
    )

    print("=== ARIMA Evaluation ===")
    print("MAE :", mae)
    print("RMSE:", rmse)
    print("\nExpected return distribution:")
    print(res["expected_ret"].describe())

    # ==================================================
    # 2️⃣ Adaptive threshold
    # ==================================================
    std = res["expected_ret"].std()
    threshold = 0.5 * std

    print(f"\nUsing threshold = {threshold:.8f}")

    # ==================================================
    # 3️⃣ Second run: real trading signals
    # ==================================================
    res, mae, rmse = arima_forecast(
        prices=prices,
        threshold=threshold,
    )

    print("\nPosition counts:")
    print(res["position"].value_counts())

    # ==================================================
    # 4️⃣ Save results
    # ==================================================
    res_out = res.copy()
    res_out["symbol"] = symbol

    out_path = out_dir / "arima_predictions.csv"
    res_out.to_csv(out_path, index=False)

    print(f"\nSaved ARIMA results to: {out_path}")
