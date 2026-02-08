DSCI 560 Lab 4 – Stock Trading Strategy
1. Project Overview
This project implements and evaluates a transaction-cost-aware stock trading strategy using intraday price data. The primary trading algorithm is a Simple Moving Average (SMA) crossover strategy, which is progressively improved using a band threshold and a cooldown mechanism to reduce over-trading. The project also explores time-series prediction metrics (MAE, RMSE) and an alternative ARIMA-based forecasting approach for comparison.

2. Requirements
• Python 3.13.5 (we used Anaconda)
• Required packages: pandas, numpy, matplotlib, yfinance, statsmodels, scipy

3. Project Structure
• data/ – CSV files containing stock price data (5-minute and 15-minute)
• src/ – Baseline strategy, backtesting engine, metrics, and plotting scripts
• improved/ – Improved strategy (added band and cooldown strategy) and related runners
• outputs/ – Generated signals, equity curves, summaries, and figures

4. How to Run the Code
Step 1: Collect price data
5-minute data: python src/collect_data.py
15-minute data: python improved/collect_data_15m.py
Step 2: Generate trading signals
Baseline SMA signals: python src/run_signals.py
Band-only SMA signals: python src/run_signals_band.py
Improved strategy (band + cooldown): python improved/run_signals_improved.py
Step 3: Run backtesting
Baseline backtest: python src/run_backtest.py
Improved backtest (5m or 15m): python improved/run_backtest_improved.py
Step 4: Plot equity curves
Improved strategy equity curves (5m): python src/plot_equity_improved_compare.py --tag 5m
Improved strategy equity curves (15m): python src/plot_equity_improved_compare.py --tag 15m

5. Evaluation Metrics
The trading strategies are evaluated using final portfolio value, annualized return, and Sharpe ratio. In addition, Mean Absolute Error (MAE) and Root Mean Squared Error (RMSE) are computed using a simple one-step-ahead naive forecast for exploratory time-series analysis.

6. ARIMA Model (Alternative Approach)
An ARIMA-based forecasting model is included as an alternative, prediction-driven approach. The ARIMA implementation performs walk-forward forecasting and reports MAE and RMSE. Due to high computational cost and sensitivity to transaction costs, ARIMA is used for comparison and analysis rather than as the final trading strategy.
Run ARIMA evaluation with: python src/run_arima.py

7. Notes
All output files, including signals, equity curves, summaries, and figures, are saved to the outputs/ directory. The improved 15-minute strategy with transaction costs represents the final model reported in the accompanying report.
<img width="432" height="646" alt="image" src="https://github.com/user-attachments/assets/fffe216e-99f3-4797-ba99-eb6f084803d3" />
