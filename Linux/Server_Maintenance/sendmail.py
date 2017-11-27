#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os
import smtplib
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.header import Header
from email.utils import formataddr


# Options
server_name = 'UBUNTU'
send_email = 'sender@domain.tld'
password = 'password'
smtp_server = 'smtp.domain.tld'
receivers = [('Admin', 'receiver@domain.tld')]


# Mailing messages
dmesg = os.popen('dmesg').read()
ifconfig = os.popen('ifconfig').read()

# More mailing options and messages
sender = {
    'address': send_email,
    'nickname': server_name,
    'password': password,
    'smtp_server': smtp_server,
    'smtp_port': 465, }

mail = {
    'content': ifconfig,
    'subject': 'Server Restarted: {}'.format(server_name),
    'attachments': [('dmesg.txt', dmesg)],
}


def sendmail(sender, receivers, mail):
    message = MIMEMultipart()
    message['From'] = formataddr((Header(sender['nickname'], 'utf-8').encode(), sender['address']))
    message['To'] = ','.join(map(lambda x: formataddr((Header(x[0], 'utf-8').encode(), x[1])), receivers))
    message['Subject'] = Header(mail['subject'], 'utf-8').encode()

    if 'content' in mail:
        message.attach(MIMEText(mail['content'], 'plain', 'utf-8'))

    if 'content_html' in mail:
        message.attach(MIMEText(mail['content_html'], 'html', 'utf-8'))

    if 'attachments' in mail:
        for attachment in mail['attachments']:
            att = MIMEText(attachment[1], 'base64', 'utf-8')
            att["Content-Type"] = "application/octet-stream"
            att["Content-Disposition"] = 'attachment; filename="{}"'.format(attachment[0])
            message.attach(att)

    if 'images' in mail:
        for image in mail['images']:
            img = MIMEImage(image['data'])
            img.add_header('Content-ID', '<{}>'.format(image['Content-ID']))
            message.attach(img)

    server = smtplib.SMTP_SSL(sender['smtp_server'], sender['smtp_port'])
    server.login(sender['address'], sender['password'])
    server.sendmail(sender['address'], list(zip(*receivers))[1], message.as_string())
    server.quit()


if __name__ == '__main__':
    sendmail(sender, receivers, mail)
