import smtplib
from email.message import EmailMessage
import os
from langchain.tools import tool

@tool
def send_email(to_email: str, subject: str, body: str):
    """Sends an email using Gmail SMTP."""
    msg = EmailMessage()
    msg.set_content(body)
    msg['Subject'] = subject
    msg['From'] = os.getenv("EMAIL_ADDRESS")
    msg['To'] = to_email

    # Connect to Gmail's Server
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(os.getenv("EMAIL_ADDRESS"), os.getenv("EMAIL_PASSWORD"))
        smtp.send_message(msg)
    return f"Email sent successfully to {to_email}!"
