from twilio.rest import Client
import os
from langchain.tools import tool

@tool
def send_whatsapp_message(to_number: str, message_body: str):
    """Sends a WhatsApp message via Twilio API."""
    try:
        account_sid = os.getenv('TWILIO_ACCOUNT_SID')
        auth_token = os.getenv('TWILIO_AUTH_TOKEN')
        client = Client(account_sid, auth_token)

        message = client.messages.create(
            from_=os.getenv('TWILIO_WHATSAPP_NUMBER'),
            body=message_body,
            to=f'whatsapp:{to_number}'
        )
        return f"✅ Message sent! SID: {message.sid}"
    except Exception as e:
        return f"❌ WhatsApp Error: {str(e)}"
