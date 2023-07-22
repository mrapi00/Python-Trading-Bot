# run bot with this script, can execute orders by 
# updating this script

import sys

from moving_average import MovingAverageStrategy
from twitter_strategy import TwitterStrategy


def main():
    if len(sys.argv) != 2:
        raise Exception("Usage: python run_bot.py <bot-name> <ticker>")
    
    args = sys.argv[1:]
    bot_name = args[0]
    ticker = args[1]

    if bot_name == "Twitter" :
        tb = TwitterStrategy()
        print(f"TwitterSentiments : {tb.make_order_recommendation(ticker)}")
    elif bot_name == "Average" :
        tb = MovingAverageStrategy()
        print(f"SimpleMovingAverage : {tb.make_order_recommendation(ticker)}")

    print(f"Current buying power : ${tb.get_buying_power()}")
    print(f"Market price of {tb.get_company_name_from_ticker(ticker)} is ${tb.get_market_price(ticker)}")


if __name__ == "__main__":
    main()