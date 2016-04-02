import smtplib	# send messages library
from Log import Log
from email.mime.text import MIMEText

class TextMessage:
	def __init__(self):
		self._to_addr = Log.to_addr
		self._from_addr = Log.from_addr
		self._authentication = Log.authentication
	
	def send_message(self, message):
		self.server = smtplib.SMTP("smtp.gmail.com:587")
		self.server.starttls()
		self.server.login(self._from_addr, self._authentication)	
		self.server.sendmail(self._from_addr, self._to_addr, MIMEText(message).as_string())
		self.server.quit()