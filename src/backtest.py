import pandas as pd

def run_backtest(
    df_signals: pd.DataFrame,
    initial_cash: float = 10_000.0,
    fee_rate: float = 0.0005,          #目前设为0，这个是交易费用
    allow_fractional: bool = False  
):

    cash = float(initial_cash)
    shares = 0.0

    equity_rows = []
    trade_rows = []

    for _, row in df_signals.iterrows():
        ts = row["timestamp"]
        price = float(row["price"])
        sig = row["signal"]

        if sig == "BUY" and shares == 0:
            # all-in 买入
            if allow_fractional:
                buy_shares = cash / price
            else:
                buy_shares = int(cash // price)

            if buy_shares > 0:
                cost = buy_shares * price
                fee = cost * fee_rate
                cash -= (cost + fee)
                shares += buy_shares

                trade_rows.append({
                    "timestamp": ts, "action": "BUY", "price": price,
                    "shares": buy_shares, "cash_after": cash
                })

        elif sig == "SELL" and shares > 0:
            # all-out 卖出
            proceeds = shares * price
            fee = proceeds * fee_rate
            cash += (proceeds - fee)

            trade_rows.append({
                "timestamp": ts, "action": "SELL", "price": price,
                "shares": shares, "cash_after": cash
            })

            shares = 0.0

        equity = cash + shares * price
        equity_rows.append({
            "timestamp": ts,
            "price": price,
            "signal": sig,
            "cash": cash,
            "shares": shares,
            "equity": equity
        })

    equity_df = pd.DataFrame(equity_rows)
    trades_df = pd.DataFrame(trade_rows)

    return equity_df, trades_df