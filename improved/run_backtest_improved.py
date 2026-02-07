from pathlib import Path
import pandas as pd
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT / "src"))

from backtest import run_backtest 
from metrics import annualized_return, sharpe_ratio 


def main():
    out_dir = ROOT / "outputs"
    out_dir.mkdir(exist_ok=True)

    signals_path = out_dir / "signals_AAPL_improved_15m.csv"
    df = pd.read_csv(signals_path)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df = df.sort_values("timestamp").reset_index(drop=True)

    periods_per_year = 252 * 26  # 15-min 数据用26，5min数据用78

    #No transaction cost
    equity_no_fee, trades_no_fee = run_backtest(
        df, initial_cash=10_000.0, fee_rate=0.0, allow_fractional=False
    )
    ann_no_fee = annualized_return(equity_no_fee["equity"], periods_per_year)
    sharpe_no_fee = sharpe_ratio(equity_no_fee["equity"], periods_per_year)

    #With transaction cost
    equity_fee, trades_fee = run_backtest(
        df, initial_cash=10_000.0, fee_rate=0.0005, allow_fractional=False
    )
    ann_fee = annualized_return(equity_fee["equity"], periods_per_year)
    sharpe_fee = sharpe_ratio(equity_fee["equity"], periods_per_year)


    equity_no_fee.to_csv(out_dir / "equity_curve_AAPL_improved_no_fee_15m.csv", index=False)
    trades_no_fee.to_csv(out_dir / "trades_AAPL_improved_no_fee_15m.csv", index=False)
    equity_fee.to_csv(out_dir / "equity_curve_AAPL_improved_fee_15m.csv", index=False)
    trades_fee.to_csv(out_dir / "trades_AAPL_improved_fee_15m.csv", index=False)

    summary_path = out_dir / "summary_AAPL_improved_15m.txt"
    with open(summary_path, "w") as f:
        f.write("IMPROVED STRATEGY (band + cooldown)\n\n")

        f.write("WITHOUT Transaction Cost\n")
        f.write(f"Final portfolio value: {equity_no_fee['equity'].iloc[-1]:.2f}\n")
        f.write(f"Number of trades: {len(trades_no_fee)}\n")
        f.write(f"Annualized return: {ann_no_fee:.4f}\n")
        f.write(f"Sharpe ratio: {sharpe_no_fee:.4f}\n\n")

        f.write("WITH Transaction Cost (0.05%)\n")
        f.write(f"Final portfolio value: {equity_fee['equity'].iloc[-1]:.2f}\n")
        f.write(f"Number of trades: {len(trades_fee)}\n")
        f.write(f"Annualized return: {ann_fee:.4f}\n")
        f.write(f"Sharpe ratio: {sharpe_fee:.4f}\n")

    print(open(summary_path).read())
    print(f"Saved to: {summary_path}")


if __name__ == "__main__":
    main()