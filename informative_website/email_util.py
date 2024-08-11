import smtplib, ssl
from email.message import EmailMessage

from email.mime.text import MIMEText

def send(to_email, token):
    from_email = 'admin'
    subject = 'forgot password'
    message = 'temporary password: ' + token
    send_email(from_email, to_email, subject, message)

def send_email(from_email, to_email, subject, message):
    email = EmailMessage()
    email['Subject'] = subject
    email['From'] = from_email
    email['To'] = to_email
    email.set_content(message)
    server = smtplib.SMTP("localhost", 1025)
    server.set_debuglevel(1)
    server.send_message(email)
    print('successfully sent email to: ', to_email)
    server.quit()
