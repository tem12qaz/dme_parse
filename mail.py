import smtplib
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formatdate


from config import EMAIL_ADDRESS, EMAIL_HOST, EMAIL_PASSWORD, EMAIL_SUBJECT, \
    EMAIL_PORT, status_messages, SIGN, SIGN_2


def send_mail(email_to, status, data, email_from=EMAIL_ADDRESS, subject=EMAIL_SUBJECT):
    email_to = [EMAIL_ADDRESS] + email_to

    text = status_messages[status].format(place=data[0], weight=data[1], to=data[2].split('->')[-1])

    if status == 1 or status == 2:
        text_2 = 'Ожидайте следующее сообщение о ходе Вашей авиа перевозки...'
    else:
        text_2 = '''Ожидайте звонок оператора грузового терминала о готовности Вашего груза к выдаче.<br><br>Обращаем Ваше внимание, на то что грузовой терминал Вашего города при получении груза может взимать терминальный сбор в соответствии с тарифами грузового терминала.<br><br><br>Перевозка завершена!  '''

    msg = MIMEMultipart()
    msg['From'] = email_from
    msg['To'] = ', '.join(email_to)
    msg['Date'] = formatdate(localtime=True)
    msg['Subject'] = subject

    html = f"""\
    <html>
      <head></head>
        <body>
           <span style="color:#1f497d;font-family:'georgia' , serif;font-size:14pt">{text}</span>
           <br>
           <span style="color:#1f497d;font-family:'georgia' , serif;font-size:14pt">{text_2}</span>
           <br>
           <br>
           <br>
           <span style="color:#1f497d;font-family:'georgia' , serif;font-size:10pt">{SIGN}</span>
           <br>
           <span style="color:#1f497d;font-family:'georgia' , serif;font-size:10pt">{SIGN_2}</span>
           <br>
           <br>
           <img src="cid:image1" alt="Logo" style="width:288px;height:150px;"><br>          
        </body>
    </html>
    """
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
