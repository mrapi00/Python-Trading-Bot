# twitter_strategy.py leverage a sentiment nlp library (vaderSentiment) 
# to make decision about buying or selling a stock

from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import pandas as pd
import tweepy
import pandas as pd
from parent_bot import Decision, BaseBot
from credentials import TwitterCredentials

BUY_SCORE_THRESH = 0.03
SELL_SCORE_THRESH = -0.03

class TwitterStrategy(BaseBot):
    def __init__(self):
        super().__init__()

        twitter_credentials = TwitterCredentials()
        auth = tweepy.AppAuthHandler(twitter_credentials.consumer_key, twitter_credentials.consumer_secret)
        self.twitter_api = tweepy.API(auth)

        self.sentiment_analyzer = SentimentIntensityAnalyzer()

    def retrieve_tweets(self, ticker, max_count=100):

        searched_tweets = []

        assert ticker, "ticker cannot be a null value"

        assert max_count > 0, "max_count must be a positive number"

        company = self.get_company_name_from_ticker(ticker)

        # Search for max_counts tweets mentioning the company.
        public_tweets = tweepy.Cursor(
            self.twitter_api.search_tweets,
            q=company,
            lang="en",
            result_type="recent",
            tweet_mode="extended",
        ).items(max_count)

        # Extract the text body of each tweet.
        searched_tweets = []

        for tweet in public_tweets:
            searched_tweets.append(tweet.full_text)

        return searched_tweets

    def analyze_tweet_sentiments(self, tweets):

        assert tweets, "param tweets cannot be a null value"

        column_names = ["tweet", "sentiment_score"]
        tweet_sentiments_df = pd.DataFrame(columns=column_names)

        for tweet in tweets:
            score = self.sentiment_analyzer.polarity_scores(tweet)["compound"]
            tweet_sentiment = {"tweet": tweet, "sentiment_score": score}
            tweet_sentiments_df = pd.concat(
                [tweet_sentiments_df, pd.DataFrame([tweet_sentiment])],
                ignore_index=True,
            )

        average_sentiment_score = tweet_sentiments_df["sentiment_score"].mean()

        return average_sentiment_score

    def make_order_recommendation(self, ticker):

        assert ticker, "param ticker cannot be a null value"

        public_tweets = self.retrieve_tweets(ticker)
        consensus_score = self.analyze_tweet_sentiments(public_tweets)

        if consensus_score >= BUY_SCORE_THRESH:
            return Decision.BUY

        elif consensus_score <= SELL_SCORE_THRESH:
            return Decision.SELL

        else:
            return Decision.HOLD