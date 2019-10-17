# coding: utf-8

import re
import smtpd
import asyncore

from email.parser import BytesParser
from email.message import Message
from datetime import datetime

from ..module import notification_input
from ..alert_input import UFVAlertInput
from .. import logging

logger = logging.get_logger(__name__)

img_mimes = {
    'image/gif': 'gif',
    'image/jpeg': 'jpg',
    'image/png': 'png',
    'image/tiff': 'tiff',
    'image/webp': 'webp',
    'image/x-ms-bmp': 'bmp',
}

class SMTPServer(smtpd.SMTPServer):

    def __init__(self, output_queue, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.output = output_queue
        logger.info('Started STMP server')

    def process_message(self, peer, mailfrom, rcpttos, data, **kwargs):

        timestamp = datetime.now()

        logger.info(
            'Notification email from UniFi Video at {}:{}. ' \
            'From: {}, To: {}'.format(
                peer[0], peer[1], mailfrom, ', '.join(rcpttos)))

        attachment_body = None

        for message in BytesParser().parsebytes(data).walk():
            content_type = message.get_content_type()
            content_id = message.get('Content-ID', '')
            if content_type in img_mimes and 'snapshot' in content_id:
                attachment_body = message.get_payload(decode=True)
                break

        if not attachment_body:
            return

        self.output.put({
            'attachments': [{
                'body': attachment_body,
                'mime': content_type,
            }],
            'exec_datetime': timestamp,
            'alert_datetime': datetime(1970, 1, 1),
            'text_content': '',
        })

def create_and_start(output_queue, addr, port):
    smtpd = SMTPServer(output_queue, (addr, port), ('127.0.0.1', 7878))
    asyncore.loop()
