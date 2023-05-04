# FINA4350

## Data preparation procedure
1. `data_preparation.ipynb` extracts tweets posted by Jim Cramer. The scraped data is saved to `/sources/data.csv`
2. `data_preparation.ipynb` extracts finance data from Yahoo Finance. The collected data is saved to `/sources/data.csv`

## Backtesting procedure
1. `fetch_madmoney.py` pulls the Mad Money stock picks from The Street website and saves them to `/data/thestreet/`
2. `prepare_backtest.ipynb` reads the Mad Money stock picks from `/data/thestreet/` and prepares the ranked top picks for backtesting. The prepared data is saved to `/data/backtest/`
3. Upload the algorithm in `quantconnect.py` to QuantConnect and run the backtest, or set up the Lean engine locally and run the backtest. The backtest results are saved to `/data/backtest/reports`
    - `cramer_v1_report`: Long 5 bottom ranked stocks and short 5 top ranked stocks
    - `cramer_v1_long_SPY_report`: Short 5 top ranked stocks and long SPY
    - `cramer_v1_short_SPY_report`: Long 5 bottom ranked stocks and short SPY
    - `cramer_follower`: TODO download the backtest results