import os
from twilio.rest import Client
from os.path import join, dirname
from dotenv import  load_dotenv

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

account_sid = os.getenv('TWILIO_SID')
auth_token = os.getenv('TWILIO_AUTH_TOKEN')
client = Client(account_sid, auth_token)

whatsapp_from = os.getenv('WHATSAPP_FROM')
whatsapp_to = os.getenv('WHATSAPP_TO')

def sendToWhatsApp(messageToUsr):
    message = client.messages \
        .create(
        from_=whatsapp_from,
        body=messageToUsr,
        to=whatsapp_to
    )

    print(message.sid)