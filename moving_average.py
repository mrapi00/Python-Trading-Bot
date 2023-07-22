# uses a moving average strategy that compares the average
# from past 200 days to past 20 days, to make decision
# to buy or sell a stock

import pandas as pd
from parent_bot import Decision, TradeBot

class MovingAverageStrategy(TradeBot):
    def __init__(self):
        super().__init__()

    def calculate_moving_average(self, stock_history_df, number_of_days):

        assert not stock_history_df, "stock_history_df cannot be null"
        assert not stock_history_df.empty, "stock_history_df cannot be empty"
        assert number_of_days >=1, "number_of_days must be a positive number"

        stock_history_df["close_price"] = pd.to_numeric(stock_history_df["close_price"], errors="coerce")
    
        n_day_stock_history = stock_history_df.tail(number_of_days)
        n_day_moving_average = round(n_day_stock_history["close_price"].mean(), 2)

        return n_day_moving_average

    def make_order_recommendation(self, ticker):

        assert ticker, "ticker cannot be null"

        stock_history_df = self.get_stock_history_df(ticker)

        moving_average_200_day = self.calculate_moving_average(stock_history_df, 200)

        moving_average_20_day = self.calculate_moving_average(stock_history_df, 20)

        # Determine the order recommendation.
        if moving_average_20_day > moving_average_200_day:
            return Decision.BUY

        elif moving_average_20_day < moving_average_200_day:
            return Decision.SELL

        else:
            return Decision.HOLD
