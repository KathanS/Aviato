from email.message import EmailMessage
import smtplib
import os
import smtplib
import ssl
from email.mime.text import MIMEText
from email.utils import formataddr
from email.mime.multipart import MIMEMultipart  # New line
from email.mime.base import MIMEBase  # New line
from email import encoders  # New line

email_sender = 'aviato.art@gmail.com'
email_password = 'wehvdrvnfnumhypq'
email_reciever = '201901026@daiict.ac.in'

email_html = open('reset_template.html')
email_body = email_html.read()

subject = 'Look what I have Done!'

body = """
Hello, mail from NJ.
"""


nj = EmailMessage()
nj['From'] = email_sender
nj['To']   = email_reciever
nj['Subject'] = subject
nj.attach(MIMEText(email_body, 'html'))

nj.set_content(body)

context = ssl.create_default_context()

with smtplib.SMTP_SSL('smtp.gmail.com',465,context = context) as smtp:
    smtp.login(email_sender,email_password)
    smtp.sendmail(email_sender,email_reciever,nj.as_string())