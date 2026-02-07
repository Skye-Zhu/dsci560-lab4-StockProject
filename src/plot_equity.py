from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

def main():
    root = Path(__file__).resolve().parents[1]
    out_dir = root / "outputs"

    no_fee_path = out_dir / "equity_curve_AAPL_no_fee.csv"
    fee_path = out_dir / "equity_curve_AAPL_fee.csv"

    no_fee = pd.read_csv(no_fee_path)
    fee = pd.read_csv(fee_path)

    no_fee["timestamp"] = pd.to_datetime(no_fee["timestamp"])
    fee["timestamp"] = pd.to_datetime(fee["timestamp"])

    plt.figure()
    plt.plot(no_fee["timestamp"], no_fee["equity"], label="No Fee")
    plt.plot(fee["timestamp"], fee["equity"], label="With Fee (0.05%)")
    plt.xlabel("Time")
    plt.ylabel("Portfolio Value ($)")
    plt.title("Equity Curve Comparison (AAPL SMA Crossover)")
    plt.legend()
    plt.tight_layout()

    fig_path = out_dir / "equity_curve_compare.png"
    plt.savefig(fig_path, dpi=200)
    print(f"Saved plot to: {fig_path}")

if __name__ == "__main__":
    main()