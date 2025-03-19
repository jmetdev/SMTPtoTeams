import smtpd
import asyncore
from email.parser import BytesParser
import requests
import os  # <---

WEBEX_TOKEN = os.getenv('WEBEX_TOKEN')  # <---
WEBEX_ROOM_ID = os.getenv('WEBEX_ROOM_ID')  # <---
WEBEX_API_URL = 'https://webexapis.com/v1/messages'


class SMTPWebexHandler(smtpd.SMTPServer):
	def process_message(self, peer, mailfrom, rcpttos, data, **kwargs):
		message = BytesParser().parsebytes(data)
		body = message.get_payload(decode=True).decode('utf-8')
		self.send_message_to_webex(body)

	def send_message_to_webex(self, message_body):
		headers = {
			'Authorization': f'Bearer {WEBEX_TOKEN}',
			'Content-Type': 'application/json',
		}
		data = {
			'roomId': WEBEX_ROOM_ID,
			'text': message_body,
		}
		response = requests.post(WEBEX_API_URL, json=data, headers=headers)
		print(response.text)


if __name__ == "__main__":
	server = SMTPWebexHandler(('0.0.0.0', 1125), None)
	try:
		asyncore.loop()
	except KeyboardInterrupt:
		pass