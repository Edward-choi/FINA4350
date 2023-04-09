# Data preparation

In this blog post, we will introduce how we prepare the financial and social data using web scrapers and APIs.

## Snscrape

Snscrape is a Python package that allows you to scrape data from various social media platforms such as Twitter, Instagram, Reddit, and more. It is an alternative to the official APIs provided by these platforms, and it uses web scraping techniques to extract data directly from the HTML source code of the websites.

One advantage of using snscrape is that it can help prevent rate limit errors, which occur when you make too many requests to an API within a certain period of time. Many social media platforms have rate limits in place to prevent abuse and ensure the stability of their services.

Snscrape can prevent rate limit errors by using a combination of features such as rate limiting, backoff strategies, and proxies. Rate limiting involves slowing down the rate at which you make requests to an API to stay within the platform's limits. Backoff strategies involve waiting for a certain period of time before making another request after receiving a rate limit error. Proxies involve using a different IP address for each request to avoid triggering rate limit restrictions.

Overall, snscrape can be a useful tool for scraping data from social media platforms while avoiding rate limit errors.

### Extract data from Twitter

To scrape data from Twitter using snscrape, we first define the cashtag (symbol for a stock or cryptocurrency) we want to search for. Then, we use the TwitterSearchScraper method from snscrape to scrape tweets that contain the cashtag. Finally, we store the scraped tweets in a pandas DataFrame and export it to a csv file.

## YFinance

Yfinance is a Python package that provides a simple and convenient way to download historical stock price data from Yahoo Finance. It allows users to easily retrieve historical stock data and financial statements, as well as real-time stock price data.

One of the advantages of yfinance is its comprehensive data coverage, which makes it a valuable tool for investors and researchers who need to analyze the performance of different financial markets and asset classes. With yfinance, users can easily download historical stock data for individual companies or for entire stock market indices, such as the S&P 500 or Dow Jones Industrial Average.

Moreover, yfinance uses multithreading to download data in parallel, which can significantly improve performance. This allows users to download large amounts of historical stock data quickly and efficiently. Additionally, yfinance's ability to download data in parallel makes it possible to retrieve data for multiple stocks or assets at once, further improving performance.

### Financial data extraction

To extract the corresponding financial data from yfinance, we use the ticker.history method to trace back the history of a given stock symbol by passing in the start and end dates as parameters. For example, yfinance.Ticker("MSFT").history(start="2020-01-01", end="2022-01-31") will return us the historical data of Microsoft in the whole January in 2020, including daily trading volume and closing prices. In particular, we extract the closing prices of the stocks on the 0th day (the day when Jim Cramer post the tweet), 30th day, 90th day and 180th day. We will further compare them and evalute the performance of the stocks.