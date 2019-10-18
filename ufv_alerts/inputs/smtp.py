import smtpd
import asyncore

from email.parser import BytesParser
from datetime import datetime

from .. import logging

logger = logging.get_logger(__name__)

img_mimes = {
    'image/jpeg': 'jpg',
    'image/png': 'png',
}

class SMTPServer(smtpd.SMTPServer):

    def __init__(self, output_queue, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.output = output_queue
        logger.info('Started STMP server')

    def process_message(self, peer, mailfrom, rcpttos, data, **kwargs):

        logger.info(
            'Notification email from UniFi Video at {}:{}. ' \
            'From: {}, To: {}'.format(
                peer[0], peer[1], mailfrom, ', '.join(rcpttos)))

        parsed = {
            'attachments': [],
            'exec_datetime': datetime.now(),
            'alert_datetime': datetime(1970, 1, 1),
            'text_content': '',
            'subject': '',
            'remote_addr': peer[0],
        }

        for message in BytesParser().parsebytes(data).walk():

            if 'Subject' in message:
                parsed['subject'] = message['Subject']

            # if 'Date' in message:
            #     print('DATE', message['Date'])
            #     parsed['alert_datetime'] = datetime.strptime(
            #         message['Date'], '%a, %d %b %Y %H:%M:%S %z')

            content_type = message.get_content_type()
            content_id = message.get('Content-ID', '')

            if content_type == 'text/plain':
                parsed['text_content'] += message.get_payload(decode=True)\
                    .decode('utf8')
            elif content_type in img_mimes and 'snapshot' in content_id:
                parsed['attachments'].append({
                    'mime': content_type,
                    'body': message.get_payload(decode=True),
                })

        self.output.put(parsed)

def create_and_start(output_queue, addr, port):
    smtpd = SMTPServer(output_queue, (addr, port), ('127.0.0.2', 0))
    asyncore.loop()
