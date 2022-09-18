import smtplib
import ssl
from email.mime.text import MIMEText
from email.utils import formataddr
from email.mime.multipart import MIMEMultipart  # New line
from email.mime.base import MIMEBase  # New line
from email import encoders  # New line

# User configuration
sender_email = 'aviato.art@gmail.com'
sender_name = 'Aviato India'
password = 'wehvdrvnfnumhypq'

receiver_emails = ['201901026@daiict.ac.in']
receiver_names = ['Kathan Sanghavi']

# Email body
email_html = open("C:\\Users\\91997\\Desktop\\email\\reset_template.html")
email_body = email_html.read()


for receiver_email, receiver_name in zip(receiver_emails, receiver_names):
		print("Sending the email...")
		# Configurating user's info
		msg = MIMEMultipart()
		msg['To'] = formataddr((receiver_name, receiver_email))
		msg['From'] = formataddr((sender_name, sender_email))
		msg['Subject'] = 'Hello, my friend ' + receiver_name
		
		msg.attach(MIMEText(email_body, 'html'))

		try:
				# Creating a SMTP session | use 587 with TLS, 465 SSL and 25
				server = smtplib.SMTP('smtp.gmail.com', 587)
				# Encrypts the email
				context = ssl.create_default_context()
				server.starttls(context=context)
				# We log in into our Google account
				server.login(sender_email, password)
				# Sending email from sender, to receiver with the email body
				server.sendmail(sender_email, receiver_email, msg.as_string())
				print('Email sent!')
		except Exception as e:
				print(f'Oh no! Something bad happened!\n{e}')
				break
		finally:
				print('Closing the server...')
				server.quit()
