import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_email(subject, body, sender, recipients, smtp_server, smtp_port, username, password):
    # Create a multipart message
    message = MIMEMultipart()
    message["Subject"] = subject
    message["From"] = sender
    message["To"] = ', '.join(recipients)

    # Add the body of the email as plain text
    message.attach(MIMEText(body, "plain"))

    # Connect to the SMTP server
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(username, password)

        # Send the email
        server.send_message(message)

# Usage example
subject = "Hello from Python"
body = "This is the body of the email."
sender = "avyaktex@gmail.com"
recipients = ["dhrumilsheth1512@gmail.com"]
smtp_server = "smtp.gmail.com"
smtp_port = 587
username = "avyaktex@gmail.com"
password = "tooxbsopcagtjfor"

send_email(subject, body, sender, recipients, smtp_server, smtp_port, username, password)