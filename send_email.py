# -*- coding:utf-8 -*-

import conf
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.application import MIMEApplication
from email import encoders

from email.header import Header
import pandas

file_path = conf.FILE_PATH
# receivers = list(pandas.read_csv(file_path)['email'])

f = open(file_path, "r")
lines = f.readlines()
receivers = []
for line in lines:
    line = line.replace('\n', '')
    line = line.replace(' ', '')
    receivers.append(line)

mail_host = conf.MAIL_HOST
mail_user = conf.MAIL_USER
mail_pwd = conf.MAIL_PWD

msg = MIMEMultipart('alternative')
msg['From'] = mail_user
msg['Subject'] = Header(conf.HEADERS, 'utf-8')

msg.attach(MIMEText('<html><body>' + conf.BODY + '</body></html>', 'html', 'utf-8'))

image_path_list = conf.IMAGE_PATH_LIST

if image_path_list:

    for image_path in image_path_list:
        image_index = image_path_list.index(image_path)
        msg.attach(
            MIMEText('<html><body>' + '<p><img src="cid:' + str(image_index) + '"></p>' + '</body></html>', 'html',
                     'utf-8'))

        image_name = conf.IMAGE_NAME_LIST[image_index]
        with open(image_path, 'rb') as f:
            mm = MIMEBase('image', image_name.split('.')[-1], filename=image_name)
            mm.add_header('Content-Disposition', 'attachment', filename=image_name)
            mm.add_header('Content-ID', '<%s>' % image_index)
            mm.add_header('X-Attachment-Id', str(image_index))
            mm.set_payload(f.read())
            encoders.encode_base64(mm)
            msg.attach(mm)

apk_path = conf.APK_PATH
if apk_path:
    apk = MIMEApplication(open(apk_path, 'rb').read())
    apk.add_header('Content-Disposition', 'attachment', filename=conf.APK_NAME)
    msg.attach(apk)

try:
    server = smtplib.SMTP()
    server.set_debuglevel(1)
    server.connect(mail_host, 25)
    server.login(mail_user, mail_pwd)
    server.sendmail(mail_user, receivers, msg.as_string())
    server.close()
    print 'Success'
except smtplib.SMTPException:
    print 'Error'
