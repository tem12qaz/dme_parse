import smtplib
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formatdate


from config import EMAIL_ADDRESS, EMAIL_HOST, EMAIL_PASSWORD, EMAIL_SUBJECT, \
    EMAIL_PORT
from text import status_messages, TEXT_2_1, TEXT_2_2, SIGN, SIGN_2, HTML


def send_mail(email_to, status, data, email_from=EMAIL_ADDRESS, subject=EMAIL_SUBJECT):
    email_to = [EMAIL_ADDRESS] + email_to

    text = status_messages[status].format(place=data[0], weight=data[1], to=data[2])

    if status == 1 or status == 2:
        text_2 = TEXT_2_1
    else:
        text_2 = TEXT_2_2

    msg = MIMEMultipart()
    msg['From'] = email_from
    msg['To'] = ', '.join(email_to)
    msg['Date'] = formatdate(localtime=True)
    msg['Subject'] = subject

    html = HTML.format(text=text, text_2=text_2, SIGN=SIGN, SIGN_2=SIGN_2)
    # Record the MIME types of text/html.
    part2 = MIMEText(html, 'html')

    # Attach parts into message container.
    msg.attach(part2)

    # This example assumes the image is in the current directory
    fp = open('logo.png', 'rb')
    msgImage = MIMEImage(fp.read())
    fp.close()

    # Define the image's ID as referenced above
    msgImage.add_header('Content-ID', '<image1>')
    msg.attach(msgImage)

    server = smtplib.SMTP_SSL(EMAIL_HOST, EMAIL_PORT)
    server.ehlo()
    server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
    server.sendmail(email_from, email_to, msg.as_string().encode('utf-8'))
    server.close()
