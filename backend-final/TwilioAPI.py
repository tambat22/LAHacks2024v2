import os
from twilio.rest import Client
from dotenv import load_dotenv

load_dotenv()

class TwilioAPI:

    def __init__(self):
        self.client = Client(os.getenv("TWILIO_ACCOUNT_SID"), os.getenv("TWILIO_AUTH_TOKEN"))

    def make_call(self, to: str, from_: str):
        call = self.client.calls.create(
            url="http://demo.twilio.com/docs/voice.xml",
            to=to,
            from_=from_
        )
        return call.sid
