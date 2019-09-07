from flask import Flask, request, redirect
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)

@app.route("/whatsapp", methods=['GET', 'POST'])
def whatsapp_reply():
    """Respond to incoming calls with a simple text message."""

    # Get the message the user sent our Twilio number
    body = request.values.get('Body', None)

        # Start our TwiML response
    resp = MessagingResponse()

    # Add a message
    resp.message("message response")

    return str(resp)

if __name__ == "__main__":
    app.run(debug=True)