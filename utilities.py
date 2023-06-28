import os

from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class RobinhoodCredentials:
    def __init__(self):
        self.user = os.getenv("ROBINHOOD_USER")
        self.password = os.getenv("ROBINHOOD_PASS")
        self.mfa_code = os.getenv("ROBINHOOD_MFA_CODE")

    @property
    def empty_credentials(self):
        """Returns True is any credential is empty; False otherwise"""

        return not (bool(self.user) and bool(self.password) and bool(self.mfa_code))
