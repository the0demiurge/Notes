#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# To add an autostart service, you may move this script to init.d first:
# `cp $filename /etc/rc.d/init.d`
# And then, use `chkconfig --add $filename`
# Or manually link it to /etc/rc.d:
# `ln -s /etc/rc.d/init.d/$filename /etc/rc.d/rc2.d/S99$filename`
# `ln -s /etc/rc.d/init.d/$filename /etc/rc.d/rc3.d/S99$filename`
# `ln -s /etc/rc.d/init.d/$filename /etc/rc.d/rc5.d/S99$filename`
# `ln -s /etc/rc.d/init.d/$filename /etc/rc.d/rc0.d/K01$filename`
# `ln -s /etc/rc.d/init.d/$filename /etc/rc.d/rc6.d/K01$filename`

from __future__ import print_function
import os
import sys
import time
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
dmesg = os.popen('dmesg -HT').read()
last = os.popen('last').read()
bootlog = open('/var/log/boot.log').read()
apt_hist = open('/var/log/apt/history.log').read()
auth = open('/var/log/auth.log').read()
syslog = open('/var/log/syslog').read()
root_history = open('/root/.bash_history').read()

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
    'subject': 'Server {}: {}'.format(server_name, ' '.format(sys.argv[1:])),
    'attachments': [
        ('dmesg.txt', dmesg),
        ('last.txt', last),
        ('boot.log.txt', bootlog),
        ('apt.history.log.txt', apt_hist),
        ('auth.log.txt', auth),
        ('syslog.txt', syslog),
        ('root_history.txt', root_history),
    ],
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

    auth_success = False
    times = 0
    while not auth_success and times < 10:
        try:
            server.login(sender['address'], sender['password'])
            auth_success = True
        except smtplib.SMTPAuthenticationError as e:
            print(e)
            print('AUTH ERROR!')
            time.sleep(10)
            times += 1

    server.sendmail(sender['address'], list(zip(*receivers))[1], message.as_string())
    server.quit()


if __name__ == '__main__':
    sendmail(sender, receivers, mail)
