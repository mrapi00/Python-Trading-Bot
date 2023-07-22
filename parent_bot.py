# parent_bot.py defines the interface and basic implementation
# of trading API that the bot executes

import pandas as pd
import pyotp
import robin_stocks.robinhood as robinhood
from enum import Enum
from credentials import AccountCredentials

class Decision(Enum):
    BUY = 0
    SELL = 1
    HOLD = 2

class BaseBot:
    def __init__(self):

        credentials = AccountCredentials()
        totp = None
        totp = pyotp.TOTP(credentials.mfa_code).now()
        robinhood.login(credentials.user, credentials.password, mfa_code=totp)

    def logout(self):
        robinhood.logout()

    def get_stocks(self):

        return robinhood.account.build_holdings()

    def get_buying_power(self):

        return float(robinhood.profiles.load_account_profile(info="buying_power"))

    def has_sufficient_funds(self, dollar_amount):

        if not dollar_amount:
            return False

        available_funds = self.get_buying_power()

        return available_funds >= dollar_amount

    def get_market_price(self, ticker):

        if not ticker:
            return 0.00

        return float(robinhood.stocks.get_latest_price(ticker, includeExtendedHours=False)[0])

    def get_company_name_from_ticker(self, ticker):

        assert ticker, "Empty Ticker"
        return robinhood.stocks.get_name_by_symbol(ticker)

    def get_stock_history_df(self, ticker, interval="day", time_span="year"):

        stock_history = robinhood.stocks.get_stock_historicals(ticker, interval=interval, span=time_span)
        return pd.DataFrame(stock_history)

    def get_equity_in_stock(self, ticker):
        stocks = self.get_stocks()

        if ticker in stocks:
            stock = stocks[ticker]
            return float(stock["equity"])

        return 0

    def has_sufficient_equity(self, ticker, dollar_amount):

        if not dollar_amount or dollar_amount <= 0:
            return False

        equity_in_stock = self.get_equity_in_stock(ticker)

        return equity_in_stock >= dollar_amount

    def place_buy_order(self, ticker, dollar_amount):

        purchase_data = {}

        assert ticker and dollar_amount, "arguments can't be null"
        assert dollar_amount >= 1, "purchase cannot be made with less than $1.00 USD."

        # check for available funds
        if self.has_sufficient_funds(dollar_amount):
            print(f"Buying ${dollar_amount} of {ticker}...")
            purchase_data.update(
                robinhood.orders.order_buy_fractional_by_price(
                    ticker,
                    dollar_amount,
                    timeInForce="gtc",
                    extendedHours=False,
                    jsonify=True,
                )
            )
            print(f"Bought ${dollar_amount} of {ticker} successfully.")

        return purchase_data

    def place_sell_order(self, ticker, dollar_amount):

        sale_data = {}

        assert ticker and dollar_amount, "Arguments cannot have null values."

        # Must have enough equity for the sale
        if self.has_sufficient_equity(ticker, dollar_amount):
            print(f"Selling ${dollar_amount} of {ticker}...")
            sale_data.update(
                robinhood.orders.order_sell_fractional_by_price(
                    ticker,
                    dollar_amount,
                    timeInForce="gtc",
                    extendedHours=False,
                    jsonify=True,
                )
            )
            print(f"Sold ${dollar_amount} of {ticker} successfully")

        return sale_data

    def buy_with_available_funds(self, ticker):

        if not ticker:
            return {}

        available_funds = self.get_buying_power()

        return self.place_buy_order(ticker, available_funds)

    def sell_entire_stock(self, ticker):

        if not ticker:
            return {}

        equity_in_stock = self. get_equity_in_stock(ticker)

        return self.place_sell_order(ticker, equity_in_stock)

    def sell_all(self):

        compiled_sale_information = []
        stocks = self.get_stocks()

        for ticker in stocks.keys():
            sale_information = self.sell_entire_stock(ticker)
            compiled_sale_information.append(sale_information)

        return compiled_sale_information

    def make_order_recommendation(self, ticker):

        return Decision.HOLD

    def trade(self, ticker, dollar_amount):

        transaction_data = {}

        action = self.make_order_recommendation(ticker)

        if action == Decision.BUY:
            purchase_details = self.place_buy_order(ticker, dollar_amount)
            transaction_data.update(purchase_details)

        elif action == Decision.SELL:
            sale_details = self.place_sell_order(ticker, dollar_amount)
            transaction_data.update(sale_details)

        else:
            print(f"Held stock for {ticker}.")

        return transaction_data