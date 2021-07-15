from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from smtplib import SMTP
from settings import *


def send_error_to_email(message: Exception):
    msg = MIMEMultipart()
    msg['Subject'] = f'Ошибка {message} в dromSearch'
    to_email = 'invoker322sf@gmail.com'

    attach_file_name = 'logs/errors.txt'
    attach_file = open(attach_file_name, 'rb')
    payload = MIMEBase('application', 'octate-stream')
    payload.set_payload(attach_file.read())
    encoders.encode_base64(payload)
    payload.add_header('Content-Decomposition', 'attachment', filename=attach_file_name)
    msg.attach(payload)

    msg.attach(MIMEText(str(message), 'plain'))

    server = SMTP('smtp.gmail.com: 587')
    server.starttls()
    server.login(EMAIL, EMAIL_PASSWORD)
    server.sendmail(EMAIL, to_email, msg.as_string())

    server.quit()
    return
