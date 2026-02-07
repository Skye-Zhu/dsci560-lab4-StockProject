from pathlib import Path
import pandas as pd

from backtest import run_backtest
from metrics import annualized_return, sharpe_ratio

def main():
    root = Path(__file__).resolve().parents[1]
    signals_path = root / "outputs" / "signals_AAPL.csv"

    df = pd.read_csv(signals_path)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df = df.sort_values("timestamp").reset_index(drop=True)

    #No fee
    equity_no_fee, trades_no_fee = run_backtest(
        df_signals=df,
        initial_cash=10_000.0,
        fee_rate=0.0,
        allow_fractional=False
    )

    #With fee (0.05%)
    equity_fee, trades_fee = run_backtest(
        df_signals=df,
        initial_cash=10_000.0,
        fee_rate=0.0005,
        allow_fractional=False
    )

    # 5分钟数据：一年大约 252 个交易日 * 78 个 5-min bar ≈ 19656
    periods_per_year = 252 * 78

    ann_ret_no_fee = annualized_return(equity_no_fee["equity"], periods_per_year)
    sharpe_no_fee = sharpe_ratio(equity_no_fee["equity"], periods_per_year)

    ann_ret_fee = annualized_return(equity_fee["equity"], periods_per_year)
    sharpe_fee = sharpe_ratio(equity_fee["equity"], periods_per_year)

    out_dir = root / "outputs"
    out_dir.mkdir(exist_ok=True)

    equity_out = out_dir / "equity_curve_AAPL.csv"
    trades_out = out_dir / "trades_AAPL.csv"
    summary_out = out_dir / "summary_AAPL.txt"

    equity_out_no_fee = out_dir / "equity_curve_AAPL_no_fee.csv"
    trades_out_no_fee = out_dir / "trades_AAPL_no_fee.csv"

    equity_out_fee = out_dir / "equity_curve_AAPL_fee.csv"
    trades_out_fee = out_dir / "trades_AAPL_fee.csv"

    equity_no_fee.to_csv(equity_out_no_fee, index=False)
    trades_no_fee.to_csv(trades_out_no_fee, index=False)

    equity_fee.to_csv(equity_out_fee, index=False)
    trades_fee.to_csv(trades_out_fee, index=False)

    final_value_no_fee = equity_no_fee["equity"].iloc[-1]
    final_value_fee = equity_fee["equity"].iloc[-1]

    with open(summary_out, "w") as f:
        f.write("Backtest WITHOUT Transaction Cost\n")
        f.write("Initial cash: 10000.0\n")
        f.write(f"Final portfolio value: {final_value_no_fee:.2f}\n")
        f.write(f"Number of trades: {len(trades_no_fee)}\n")
        f.write(f"Annualized return (approx): {ann_ret_no_fee:.4f}\n")
        f.write(f"Sharpe ratio (approx): {sharpe_no_fee:.4f}\n\n")

        f.write("Backtest WITH Transaction Cost (0.05%)\n")
        f.write("Initial cash: 10000.0\n")
        f.write(f"Final portfolio value: {final_value_fee:.2f}\n")
        f.write(f"Number of trades: {len(trades_fee)}\n")
        f.write(f"Annualized return (approx): {ann_ret_fee:.4f}\n")
        f.write(f"Sharpe ratio (approx): {sharpe_fee:.4f}\n")

    print("Backtest Done")
    print(f"Equity curve (no fee) saved to: {equity_out_no_fee}")
    print(f"Trades      (no fee) saved to: {trades_out_no_fee}")
    print(f"Equity curve (fee)    saved to: {equity_out_fee}")
    print(f"Trades      (fee)    saved to: {trades_out_fee}")
    print(f"Summary saved to:            {summary_out}")
    print("\nSummary:")
    print(open(summary_out).read())

if __name__ == "__main__":
    main()