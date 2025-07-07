import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

def send_verification_email(to_email, username, token):
    from_email = os.getenv("EMAIL_USER")
    app_password = os.getenv("EMAIL_PASS")

    subject = "Verify your account"
    verification_link = f"http://127.0.0.1:5000/verify/{token}"
    body = f"""
    Hi {username},

    Thanks for registering! Please verify your email by clicking the link below:

    {verification_link}

    If you didn't sign up, you can ignore this email.
    """

    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(from_email, app_password)
            server.send_message(msg)
        print(f"Verification email sent to {to_email}")
        return True
    except Exception as e:
        print(f"Failed to send email: {e}")
        return False
