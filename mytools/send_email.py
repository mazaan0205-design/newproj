import smtplib
from email.mime.text import MIMEText
from langchain.tools import tool


GMAIL_EMAIL = "m.azaan0205@gmail.com"
GMAIL_APP_PASSWORD = "doll tmym yltj zvjm"

@tool
def send_email(recipient: str, subject: str, body: str) -> str:
    """Send an email using Gmail."""

    try:
        msg = MIMEText(body)
        msg["Subject"] = subject
        msg["From"] = GMAIL_EMAIL
        msg["To"] = recipient

        server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
        server.login(GMAIL_EMAIL, GMAIL_APP_PASSWORD)

        server.sendmail(GMAIL_EMAIL, recipient, msg.as_string())

        server.quit()

        return "Email sent successfully."

    except Exception as e:
        return f"Error sending email: {str(e)}"
    

if __name__== "__main__":
    output=send_email(recipient="rzi.codealigned@gmail.com",subject="TEST EMAIL AGENT", body="This is a test email.")
    print(output)