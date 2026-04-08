import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import streamlit as st
from langchain.tools import tool

@tool
def send_email(recipient_email: str, subject: str, body: str):
    """Sends an email using Gmail SMTP."""
    sender_email = st.secrets["EMAIL_ADDRESS"]
    password = st.secrets["EMAIL_PASSWORD"]

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, password)
        server.send_message(msg)
        server.quit()
        return "✅ Email sent successfully!"
    except Exception as e:
        return f"❌ Email Error: {str(e)}"
