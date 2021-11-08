import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formatdate


from config import EMAIL_ADDRESS, EMAIL_HOST, EMAIL_PASSWORD, EMAIL_SUBJECT, \
    EMAIL_PORT, status_messages


def send_mail(email_to, status, data, email_from=EMAIL_ADDRESS, subject=EMAIL_SUBJECT):
    email_to = EMAIL_ADDRESS + email_to

    text = status_messages[status].format(place=data[0], weight=data[1], to=data[2])

    msg = MIMEMultipart()
    msg['From'] = email_from
    msg['To'] = ', '.join(email_to)
    msg['Date'] = formatdate(localtime=True)
    msg['Subject'] = subject

    msg.attach(MIMEText(text))

    server = smtplib.SMTP_SSL(EMAIL_HOST, EMAIL_PORT)
    server.ehlo()
    server.login(email_from, EMAIL_PASSWORD)
    server.sendmail(email_from, email_to, msg.as_string())
    server.close()
