import pywhatkit
from langchain_core.tools import tool
from datetime import datetime

# 1. Define the WhatsApp Tool
@tool
def send_whatsapp_message(phone_number: str, message: str):
    """
    Sends a WhatsApp message immediately using pywhatkit.
    phone_number must include country code (e.g., '+923218417000
    ').
    """
    try:
        # send_instant_message sends it immediately
        # Note: This will open a browser tab and require you to be logged into WhatsApp Web
        pywhatkit.sendwhatmsg_instantly(phone_number, message, wait_time=60, tab_close=True)
        return f"WhatsApp message sent successfully to {phone_number}"
    except Exception as e:
        return f"Error sending WhatsApp message: {str(e)}"


# send_whatsapp_message("+923134549651","Hi this is a sample text message") 
# send_whatsapp_message("+923218417000","Hi this is a sample text message") 
# send_whatsapp_message("+923218417000","Hi this is a sample text message") 
