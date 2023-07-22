# store robinhood and twitter account credentials in OS ENV 
# so for example "export ROBINHOOD_USER=<user>"

import os

from dotenv import load_dotenv

load_dotenv()

# twitter key and secret here
class TwitterCredentials:
    def __init__(self):
        self.consumer_key = os.getenv("TWITTER_KEY")
        self.consumer_secret = os.getenv("TWITTER_SECRET")

    @property
    def empty_credentials(self):
        return not (bool(self.consumer_key) and bool(self.consumer_secret))

# robinhood credentials here
class RobinhoodCredentials:
    def __init__(self):
        self.user = os.getenv("ROBINHOOD_USER")
        self.password = os.getenv("ROBINHOOD_PW")
        self.mfa_code = os.getenv("ROBINHOOD_MFA")

    @property
    def empty_credentials(self):
        return not (bool(self.user) and bool(self.password) and bool(self.mfa_code))
