"""
A QuantConnect algorithm that implements the Cramer's Top Picks strategy.
Modify the rebalance function to customize the strategy.
"""


from AlgorithmImports import *
import pandas as pd
import ast
from datetime import datetime, timedelta
import re
from io import StringIO


CSV_PATH = "https://raw.githubusercontent.com/Edward-choi/FINA4350/main/data/backtest/cramer_top_picks_2017-2022.csv"

class CramerStock(PythonData):
    """
    "remarC" Strategy Specification

    Period:
    - Jan 2017 - Dec 2021

    Portfolio Specifications:
    - Rebalance weekly
    - an equal-weighted portfolio
    - Start of each month: buy 5 and sell 5
    - Rank = frequency * sentiment (defined in prepare_backtest.ipynb)

    Experiments:
    - (L/S) Long bottom 5 picks, Short top 5 picks 
    - (L) Long bottom 5 picks, Short SPY 
    - (S) Short top 5 picks, Long SPY
    """

    def __init__(self):
        self.Algorithm = None


    def GetSource(self, config, date, isLiveMode):
        # config.SetParameter("algorithm", self.Algorithm)
        return SubscriptionDataSource(CSV_PATH, SubscriptionTransportMedium.RemoteFile)


    def Reader(self, config, line, date, isLiveMode):
        # algorithm = config.GetParameter("algorithm")

        if not (line.strip() and line[0].isdigit()):
            return None
        
        index = CramerStock()
        index.Symbol = config.Symbol
        index.Date = date
        
        # Parse the CSV line
        date_str, top5_str, bottom5_str = re.split(',(?![^[]*\])', line)
        index.Date = datetime.strptime(date_str, "%Y-%m-%d").date()
        index.Top5 = eval(eval(top5_str))
        index.Bottom5 = eval(eval(bottom5_str))

        if self.Algorithm is not None:
            self.Algorithm.Debug(f"Reader: Date {index.Date}, Top5 {index.Top5}, Bottom5 {index.Bottom5}")

        return index

class CramerInversePerformance(QCAlgorithm):

    def __init__(self):
        self.top5 = []
        self.bottom5 = []


    def Initialize(self):
        self.SetStartDate(2017, 2, 1)
        self.SetEndDate(2021, 12, 31)
        self.SetCash(100000)
        self.UniverseSettings.Resolution = Resolution.Daily

        # Add equity universe with a custom filter (use symbols from the dataframe)
        self.AddEquity("SPY", Resolution.Daily)
        self.SetBenchmark("SPY")
        # cramer_stock = self.AddData(CramerStock, "CramerStock")
        # cramer_stock.Algorithm = self
        csv_content = self.Download(CSV_PATH)
        self.cramer_data = pd.read_csv(StringIO(csv_content), parse_dates=["Date"], index_col="Date")

        self.AddUniverse(self.CoarseSelectionFunction)
        # Schedule rebalancing weekly
        self.Schedule.On(self.DateRules.WeekStart(), self.TimeRules.AfterMarketOpen("SPY"), self.Rebalance)


    def CoarseSelectionFunction(self, coarse):
        # Get the Top5 and Bottom5 stocks for the previous month
        last_month = self.Time - timedelta(days=30)
        filtered_data = self.cramer_data.loc[self.cramer_data.index <= last_month]

        coarse_symbols = [c.Symbol.Value for c in coarse]

        if not filtered_data.empty:
            data = filtered_data.iloc[-1]
            self.top5 = [symbol for symbol in eval(data['Top5']) if symbol in coarse_symbols]
            self.bottom5 = [symbol for symbol in eval(data['Bottom5']) if symbol in coarse_symbols]
            selected_symbols = self.top5 + self.bottom5
        else:
            selected_symbols = []
        
        # selected_symbols = ['AAPL', 'GOOG', 'JPM']
        filtered_symbols = [c.Symbol for c in coarse if c.Symbol.Value in selected_symbols]
        # filtered_symbols = [x.Symbol for x in coarse if x.HasFundamentalData and x.Volume > 0 and x.DollarVolume > 500000000]
        self.Debug(f"CoarseSelectionFunction selected_symbols: {selected_symbols}")

        return filtered_symbols


    def OnData(self, data):
        if self.IsWarmingUp:
            return


    def Rebalance(self):
        # Get the Top5 and Bottom5 stocks for the previous month
        last_month = self.Time - timedelta(days=30)
        # all_symbols = list(self.ActiveSecurities)
        # self.Debug(f"all symbols: {all_symbols}")
        self.top5 = self.GetTop5(last_month)
        # self.top5 = ['SPY']
        self.bottom5 = self.GetBottom5(last_month)
        # self.bottom5 = ['SPY']
        # Log the Top5 and Bottom5 lists
        self.Debug(f"Date: {self.Time}, Top5: {self.top5}, Bottom5: {self.bottom5}")

        # Add symbols to the universe if they are not already there
        for symbol in self.top5 + self.bottom5:
            if not self.Securities.ContainsKey(symbol):
                self.AddEquity(symbol, Resolution.Daily)


        # Liquidate any stocks that are no longer in Top5 or Bottom5
        for holding in self.Portfolio.Values:
            if holding.Symbol.Value not in self.top5 and holding.Symbol.Value not in self.bottom5:
                self.Liquidate(holding.Symbol)

        
        # Calculate available margin
        total_margin = self.Portfolio.MarginRemaining
        long_margin = total_margin / 2
        short_margin = total_margin / 2

        # Open short positions in Top5 stocks and long positions in Bottom5 stocks
        if len(self.top5) > 0:
            short_weight = short_margin / len(self.top5) / self.Portfolio.TotalPortfolioValue
            self.Debug(f"Setting holdings of {self.top5} to {-short_weight}")
            for symbol in self.top5:
                self.SetHoldings(symbol, -short_weight)

        if len(self.bottom5) > 0:
            long_weight = long_margin / len(self.bottom5) / self.Portfolio.TotalPortfolioValue
            self.Debug(f"Setting holdings of {self.bottom5} to {long_weight}")
            for symbol in self.bottom5:
                self.SetHoldings(symbol, long_weight)


    def GetTop5(self, date):
        filtered_data = self.cramer_data.loc[self.cramer_data.index <= date]

        if not filtered_data.empty:
            data = filtered_data.iloc[-1]
            self.Debug(f"GetTop5: Top5 found for date {date}: {data.Top5}")
            return eval(data['Top5'])
        else:
            self.Debug(f"GetTop5: No data found for date {date}")
            return []


    def GetBottom5(self, date):
        filtered_data = self.cramer_data.loc[self.cramer_data.index <= date]

        if not filtered_data.empty:
            data = filtered_data.iloc[-1]
            self.Debug(f"GetBottom5: Bottom5 found for date {date}: {data.Bottom5}")
            return eval(data['Bottom5'])
        else:
            self.Debug(f"GetBottom5: No data found for date {date}")
            return []
