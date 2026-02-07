from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import argparse


def load_equity(path: Path) -> pd.DataFrame:
    df = pd.read_csv(path)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    return df.sort_values("timestamp").reset_index(drop=True)


def plot(tag: str):
    root = Path(__file__).resolve().parents[1]
    out_dir = root / "outputs"

    if tag == "5m":
        no_fee = out_dir / "equity_curve_AAPL_improved_no_fee.csv"
        fee = out_dir / "equity_curve_AAPL_improved_fee.csv"
        out_png = out_dir / "equity_curve_compare_improved_5m.png"
        title = "Improved Strategy Equity Curve (5-minute)"

    elif tag == "15m":
        no_fee = out_dir / "equity_curve_AAPL_improved_no_fee_15m.csv"
        fee = out_dir / "equity_curve_AAPL_improved_fee_15m.csv"
        out_png = out_dir / "equity_curve_compare_improved_15m.png"
        title = "Improved Strategy Equity Curve (15-minute)"

    else:
        raise ValueError("tag must be '5m' or '15m'")

    df_no_fee = load_equity(no_fee)
    df_fee = load_equity(fee)

    plt.figure()
    plt.plot(df_no_fee["timestamp"], df_no_fee["equity"], label="No Fee")
    plt.plot(df_fee["timestamp"], df_fee["equity"], label="With Fee (0.05%)")
    plt.xlabel("Time")
    plt.ylabel("Portfolio Value ($)")
    plt.title(title)
    plt.legend()
    plt.tight_layout()
    plt.savefig(out_png, dpi=200)

    print(f"Saved plot to: {out_png}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--tag", choices=["5m", "15m"], required=True)
    args = parser.parse_args()

    plot(args.tag)


if __name__ == "__main__":
    main()