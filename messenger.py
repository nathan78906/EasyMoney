import os
from twilio.rest import Client
from os.path import join, dirname
from dotenv import  load_dotenv

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

account_sid = os.getenv('TWILIO_SID')
auth_token = os.getenv('TWILIO_AUTH_TOKEN')
client = Client(account_sid, auth_token)

text_from = os.getenv('TEXT_FROM')
text_to = os.getenv('TEXT_TO')

def sendText(txtToUser):
    message = client.messages.create(
        body=txtToUser,
        from_=text_from,
        to=text_to
    )
    print(message.sid)