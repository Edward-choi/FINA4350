# FINA4350 - Inverse Cramer with Sentiment Analysis

This project investigates the so-called "inverse Cramer effect," which claims that stock performance is negatively correlated with Jim Cramer's recommendations. The primary goal is to determine whether this effect truly exists or if it is a mere result of selection bias. We use sentiment analysis and backtesting to test the inverse Cramer strategy and evaluate its performance over a specified time frame.

## Data Collection

`fetch_madmoney.py` pulls the Mad Money stock picks from The Street website and saves them to `/data/thestreet/` by web scraping TheStreet.com using Playwright and BeautifulSoup. The data collected includes stock symbols, recommendation dates, and sentiment scores. We store the extracted information in a structured format, such as a CSV file, for further analysis.

To gather relevant tweets from Jim Cramer, we use the `snscrape` library to scrape data from his Twitter account. We collect tweets containing stock symbols and their respective timestamps within a specified date range. The collected data is preprocessed, cleaned, and stored in a Pandas DataFrame for subsequent analysis. When the Twitter Search API is disabled for clients not logging in, we scrape nitter.net manually instead via `/experiments/fetch_tweets.ipynb`


## Backtesting procedure
1. `prepare_backtest.ipynb` reads the Mad Money stock picks from `/data/thestreet/` and prepares the ranked top picks for backtesting. The prepared data is saved to `/data/backtest/`
2. Upload the algorithm in `quantconnect.py` to QuantConnect and run the backtest, or set up the Lean engine locally and run the backtest. The backtest results are saved to `/data/backtest/reports`
    - `cramer_v1_report`: Long 5 bottom ranked stocks and short 5 top ranked stocks
    - `cramer_v1_long_SPY_report`: Short 5 top ranked stocks and long SPY
    - `cramer_v1_short_SPY_report`: Long 5 bottom ranked stocks and short SPY

Details are further described in the report.