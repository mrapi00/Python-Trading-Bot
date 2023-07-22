# Python Trading Bot

Uses the Robinhood API to automate trades within a personal Robinhood account.
Currently implement two strategies, one which uses moving average and another which use twitter sentiment analysis (using vaderSentiment). 

``` sh
export TWITTER_KEY=<consumer-key>
export TWITTER_SECRET=<consumer-secret>
export ROBINHOOD_USER=<robinhood username>
export ROBINHOOD_PW=<robinhood password>
export ROBINHOOD_MFA=<robinhood mfa code>

# run twitter sentiment analysis to make decision on Apple stock
python runbot.py Twitter AAPL
```

