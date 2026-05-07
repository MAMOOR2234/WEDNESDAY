"""Email skill for Wednesday — send emails via Gmail SMTP."""
import email
import sys
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import email.utils 

if sys.platform == "win32":
    from skills import BaseSkill
else:
    from . import BaseSkill


class Skill(BaseSkill):
    name = "Email"
    description = "Send an email via Gmail"

    def execute(self, args):
        to      = args.get("to", "").strip()
        subject = args.get("subject", "Message from Wednesday").strip()
        body    = args.get("body", "").strip()

        if not to:
            return "Who should I send the email to? Provide a 'to' address."
        if not body:
            return "What should the email say? Provide a 'body'."

        sender   = os.getenv("EMAIL_ADDRESS", "mamoorahmad6@gmail.com")
        password = os.getenv("EMAIL_PASSWORD", "")

        if not sender or not password:
            return (
                "Email not configured. Add EMAIL_ADDRESS and EMAIL_PASSWORD "
                "(Gmail App Password) to your .env file."
            )

        try:
            msg = MIMEMultipart()
            msg["From"]    = sender
            msg["To"]      = to
            msg["Subject"] = subject
            msg.attach(MIMEText(body, "plain"))

            with smtplib.SMTP("smtp.gmail.com", 587, timeout=15) as server:
                server.ehlo()
                server.starttls()
                server.login(sender, password)
                server.sendmail(sender, to, msg.as_string())

            return f"Email sent to {to} successfully!"
        except smtplib.SMTPAuthenticationError:
            return "Authentication failed. Make sure you're using a Gmail App Password, not your regular password."
        except Exception as e:
            return f"Failed to send email: {e}"
