import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from typing import *


class MailDraft:
    def __init__(self, title, sender, receivers):
        self.title = title
        self.sender = sender
        self.receivers = receivers  # [""]
        
        #
        # @ imgLst: [{'path': file path, 'name': file name}]
        # @ fileLst: [{'path': , 'name': }]
        #
        self.msg = ""
        self.imgLst = []
        self.fileLst = []

    def _send_draft(self, smtpObj):
        message = MIMEMultipart()
        message['Subject'] = self.title
        message['From'] = self.sender
        message['To'] = ','.join(self.receivers)

        content = MIMEText(self.msg, 'plain', 'utf-8')
        message.attach(content)

        for i in self.imgLst:
            message.attach(self._make_img(i['path'], i['name']))

        for i in self.fileLst:
            message.attach(self._make_file(i['path'], i['name']))

        try:
            smtpObj.sendmail(self.sender, self.receivers, message.as_string())
            print('\n==================================\n'
                  'message is sent successfully!')
        except smtplib.SMTPException as e:
            print('Error: ', e)

    def add_msg(self, newMsg):
        self.msg = self.msg + newMsg

    def add_img(self, newImgLst: List):
        self.imgLst.extend(newImgLst)

    def add_file(self, newFileLst: List):
        self.fileLst.extend(newFileLst)

    def _make_img(self, imgPath, imgName):
        with open(imgPath, 'rb') as fp:
            img = MIMEImage(fp.read())
        img['Content-Type'] = 'application/octet-stream'
        img['Content-Disposition'] = 'attachment;filename="%s"' % (imgName)
        return img

    def _make_file(self, fPath, fName):
        with open(fPath, 'rb') as fp:
            content = fp.read()
        f = MIMEText(content, 'plain', 'utf-8')
        f['Content-Type'] = 'application/octet-stream'
        f['Content-Disposition'] = 'attachment;filename="%s"' % (fName)
        return f

    # TODO:
    def _check_path(self, path):
        #
        # 检查路径是 dir 还是 file (file / image)
        # 如果是 dir，则需要将目录下的文件提取并 return
        #
        return fileList


class Mail:
    def __init__(self, host, userName, pwd):
        try:
            if 'qq' in host:
                self.smtpObj = smtplib.SMTP_SSL(host)
            else:
                # 启动
                self.smtpObj = smtplib.SMTP()
                # 连接到服务器
                self.smtpObj.connect(host, 25)
            self.smtpObj.login(userName, pwd)
        except smtplib.SMTPException as e:
            print('Error: ', e)

        self.mailLst = []

    def create_mail(self, title, sender, receivers):
        draft = MailDraft(title, sender, receivers)
        self.mailLst.append(draft)

    def _find_mail_title(self, title):
        for i in self.mailLst:
            if i.title == title:
                return self.mailLst.index(i)
        return -1

    def add_msg(self, title, newMsg):
        idx = self._find_mail_title(title)
        if idx != -1:
            self.mailLst[idx].add_msg(newMsg)

    def add_img(self, title, newImgLst):
        idx = self._find_mail_title(title)
        if idx != -1:
            self.mailLst[idx].add_img(newImgLst)

    def add_file(self, title, newFileLst):
        idx = self._find_mail_title(title)
        if idx != -1:
            self.mailLst[idx].add_file(newFileLst)

    def list_drafts(self):
        for i in self.mailLst:
            print(i.title)

    def send_mail(self, title):
        idx = self._find_mail_title(title)
        if idx != -1:
            self.mailLst[idx]._send_draft(self.smtpObj)
            del self.mailLst[idx]

    def send_all(self):
        for i in self.mailLst:
            i._send_draft(self.smtpObj)
        self.mailLst = []

    def logout(self):
        self.smtpObj.quit()

