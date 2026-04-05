import smtplib
from email.message import EmailMessage
import os
from langchain.tools import tool

@tool
def send_email(to_email: str, subject: str, body: str):
    """Sends an email using Gmail SMTP."""
    try:
        msg = EmailMessage()
        msg.set_content(body)
        msg['Subject'] = subject
        msg['From'] = os.getenv("EMAIL_ADDRESS")
        msg['To'] = to_email

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(os.getenv("EMAIL_ADDRESS"), os.getenv("EMAIL_PASSWORD"))
            smtp.send_message(msg)
        return f"✅ Email sent to {to_email}!"
    except Exception as e:
        return f"❌ Email Error: {str(e)}"
