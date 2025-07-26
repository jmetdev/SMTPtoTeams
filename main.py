import asyncio
from aiosmtpd.controller import Controller
from aiosmtpd.smtp import SMTP
from email.parser import BytesParser
import requests
import os  # <---

WEBEX_TOKEN = os.getenv('WEBEX_TOKEN')  # <---
WEBEX_ROOM_ID = os.getenv('WEBEX_ROOM_ID')  # <---
WEBEX_API_URL = 'https://webexapis.com/v1/messages'


class SMTPWebexHandler:
	def handle_RCPT(self, server, session, envelope, address, rcpt_options):
		if not address.endswith('@example.com'):
			return '550 not relaying to that domain'
		envelope.rcpt_tos.append(address)
		return '250 OK'

	def handle_DATA(self, server, session, envelope):
		message = BytesParser().parsebytes(envelope.content)
		body = message.get_payload(decode=True).decode('utf-8')
		self.send_message_to_webex(body)
		return '250 Message accepted for delivery'

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
	handler = SMTPWebexHandler()
	controller = Controller(handler, hostname='0.0.0.0', port=5001)
	controller.start()
	try:
		asyncio.get_event_loop().run_forever()
	except KeyboardInterrupt:
		controller.stop()