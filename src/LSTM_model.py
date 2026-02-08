import pandas as pd
import numpy as np

df = pd.read_csv("prices.csv")
df = df.sort_values("timestamp")
prices = df["price"].values.reshape(-1,1)

def moving_average(prices, windows):
    return pd.Series(prices.flatten()).rolling(windows).mean()

short = 20
long = 50

ma_short = moving_average(prices, short)
ma_long = moving_average(prices, long)

signals = np.zeros(len(prices))

for i in range(len(prices)):
    if ma_short[i] > ma_long[i]:
        signals = 1
    elif ma_short[i] < ma_long[i]:
        signals = -1


from sklearn.preprocessing import MinMaxScaler

scaler = MinMaxScaler(feature_range=(0,1))
prices_scaled = scaler.fit_transform(prices)

def create_sequences(data, lookback=60):
    X, y = [], []
    for i in range(lookback, len(data)):
        X.append(data[i-lookback:i, 0])
        y.append(data[i, 0])
    return np.array(X), np.array(y)

LOOKBACK = 60
X, y = create_sequences(prices_scaled, LOOKBACK)
X = X.reshape((X.shape[0], X.shape[1], 1))

split = int(len(X) * 0.8)
X_train, X_test = X[:split], X[split:]
y_train, y_test = y[:split], y[split:]


from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
from tensorflow.keras.optimizers import Adam


model = Sequential([
    LSTM(50, return_sequences=True, input_shape=(LOOKBACK, 1)),
    Dropout(0.2),
    LSTM(50),
    Dropout(0.2),
    Dense(1)])

model.compile(optimizer=Adam(learning_rate=0.001),
              loss="mse")

model.fit(X_train,
          y_train,
          epochs=20,
          batch_size=32,
          validation_split=0.1)

pred_scaled = model.predict(X_test)
pred_prices = scaler.inverse_transform(pred_scaled)
true_prices = scaler.inverse_transform(y_test.reshape(-1, 1))


signals_lstm = len(df)*["HOLD"]

for i in range(len(pred_prices)):
    if pred_prices[i] > true_prices[i] * 1.005:
        signals_lstm[i] = 1     
    elif pred_prices[i] < true_prices[i] * 0.998:
        signals_lstm[i] = -1    
    else:
        signals_lstm[i] = 0  


def map_signal(x):
    if x == 1:
        return "BUY"
    if x == -1:
        return "SELL"
    else:
        return "HOLD"

comparison_df = pd.DataFrame({
    "timestamp": df["timestamp"],
    "price": df["price"],
    "signal": signals_lstm
})

comparison_df["signal"] = comparison_df["signal"].apply(map_signal)

from backtest import run_backtest

equity_no_fee, trades_no_fee = run_backtest(
    df_signals=comparison_df,
    initial_cash=10_000.0,
    fee_rate=0.0,
    allow_fractional=False
)

equity_with_fee, trades_with_fee = run_backtest(
    df_signals=comparison_df,
    initial_cash=10_000.0,
    fee_rate=0.002,
    allow_fractional=False
)