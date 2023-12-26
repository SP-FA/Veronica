import smtplib
import imaplib
import email
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from email.header import decode_header
from typing import *
from tqdm import tqdm


class MailDraft:
    """ 用于存储 邮件信息 的类

    Attributes:
        IMG_EXT (List[str]): 常见的图片格式后缀

        title (str): 邮件的主题
        sender (str): 发件人
        receivers (List[str]): 收件人，可以包含多个
        msg (str): 邮件的内容
        attachments (List[str]): 附件的目录
        id (str): 收件箱内邮件的 id
    """
    IMG_EXT = ["jpg", "png", "jpeg", "gif"]

    def __init__(self, title, sender, receivers, msg="", attachments=[]):
        self.title = title
        self.sender = sender
        self.receivers = receivers  # [""]
        self.msg = msg
        self.attachments = attachments
        self.id = ""

    def send_draft(self, smtpObj):
        message = MIMEMultipart()
        message['Subject'] = self.title
        message['From'] = self.sender
        message['To'] = ','.join(self.receivers)

        content = MIMEText(self.msg, 'plain', 'utf-8')
        message.attach(content)

        for attachment in self.attachments:
            files = self._check_path(attachment)
            for file in files:
                message.attach(file)

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

    def _check_path(self, path) -> List[MIMENonMultipart]:
        """检查路径是 dir 还是 file (file / image)，如果是 dir 则提取目录下的文件，否则直接提取该文件

        Args:
            path (str): 文件 / 目录 路径

        Returns:
            List[MIMENonMultipart]: 一个列表，存放所有提取到的文件
        """
        if not os.path.exists(path): return []

        fileList = []
        if os.path.isdir(path):
            files = os.listdir(path)
            for f in files:
                fl = self._check_path(os.path.join(path, f))
                fileLst.extend(fl)
        else:
            _, name = os.path.split(path)
            splitName = name.split(".")
            if splitName[-1].lower() in self.IMG_EXT:
                file = self._make_img(path, name)
            else:
                file = self._make_file(path, name)
            fileList.append(file)
        return fileList

    @staticmethod
    def _make_img(self, imgPath, imgName):
        with open(imgPath, 'rb') as fp:
            img = MIMEImage(fp.read())
            img['Content-Type'] = 'application/octet-stream'
            img['Content-Disposition'] = f'attachment;filename="{imgName}"'
        return img

    @staticmethod
    def _make_file(self, fPath, fName):
        with open(fPath, 'rb') as fp:
            content = fp.read()
            f = MIMEText(content, 'plain', 'utf-8')
            f['Content-Type'] = 'application/octet-stream'
            f['Content-Disposition'] = f'attachment;filename="{fName}"'
        return f

    def __str__(self):
        return self.isChinese()
        # m = len("=========================================================")
        # msgLst = self.msg.split("\n")
        # final_title = "Subject: " + self.title
        # final_sender = "Sender : " + self.sender
        # final_msg = []
        # for msg in msgLst:
        #     section = msg.split(" ")
        #     temp_msg = ""
        #     for word in section:
        #         if len(temp_msg + word + " ") <= m:
        #             temp_msg = temp_msg + word + " "
        #         else:
        #             final_msg.append(temp_msg + " " * (m - len(temp_msg)))
        #             temp_msg = word
        #     final_msg.append(temp_msg + " " * (m - len(temp_msg)))
        #     final_msg.append(" " * m)
        # final_title_str = final_title + " " * (m - len(final_title))
        # final_sender_str = final_sender + " " * (m - len(final_sender))
        # final_msg_str = "  |\n|  ".join(final_msg)
        # final_msg_str += "  |\n==============================================================="
        #
        # return (f"=============================Draft=============================\n"
        #         f"|                                                             |\n"
        #         f"|  {final_title_str}  |\n"
        #         f"|  {final_sender_str}  |\n"
        #         f"|  ---------------------------------------------------------  |\n"
        #         f"|                                                             |\n"
        #         f"|  {final_msg_str}")

    def isChinese(self):
        m = len("=========================================================")
        msg = self.msg.replace("\r", "")
        msgLst = msg.split("\n")
        final_title = "Subject: " + self.title
        final_sender = "Sender : " + self.sender
        final_msg = []
        for msg in msgLst:
            section = [char for char in msg]
            temp_msg = ""
            for word in section:
                if len(temp_msg) + len(word) * 2 + 1 <= m:
                    temp_msg = temp_msg + word
                else:
                    final_msg.append(temp_msg + " " * ((m - len(temp_msg)) // 2))
                    temp_msg = word
            final_msg.append(temp_msg + " " * ((m - len(temp_msg)) // 2))
            final_msg.append(" " * m)
        final_title_str = final_title + " " * ((m - len(final_title)) // 2)
        final_sender_str = final_sender + " " * ((m - len(final_sender)) // 2)
        final_msg_str = "  |\n|  ".join(final_msg)
        final_msg_str += "  |\n==============================================================="

        return (f"=============================Draft=============================\n"
                f"|                                                             |\n"
                f"|  {final_title_str}  |\n"
                f"|  {final_sender_str}  |\n"
                f"|  ---------------------------------------------------------  |\n"
                f"|                                                             |\n"
                f"|  {final_msg_str}")


class MailBox:
    """ 维护一个邮箱，支持收发邮件

    Attributes:
        smtpObj (SMTP): 用来发邮件的 object
        imapObj (IMAP4): 用来接收邮件的 object
        draftLst (List[MailDraft]): 用来存储待发送的邮件
        emailLst (List[MailDraft]): 用来存储收到的邮件
        emailIDLst (List[str]): 用来存储收到邮件的 id，用来避免重复接收同一个邮件
        unreadMailIDLst (List[str]): 未读邮件列表
    """
    def __init__(self, host: str, username: str, pwd: str):
        # 发件箱
        try:
            if 'qq' in host:
                self.smtpObj = smtplib.SMTP_SSL(host)
            else:
                # 启动
                self.smtpObj = smtplib.SMTP()
                # 连接到服务器
                self.smtpObj.connect(host, 25)
            self.smtpObj.login(username, pwd)
        except smtplib.SMTPException as e:
            print('Error: ', e)

        # 收件箱
        imap_port = 993
        self.imapObj = imaplib.IMAP4_SSL(host, imap_port)
        self.imapObj.login(username, pwd)
        self.imapObj.select("inbox")

        self.draftLst = []
        self.emailLst = []
        self.emailIDLst = []
        self.unreadMailIDLst = []

    def add_draft(self, draft: MailDraft):
        self.draftLst.append(draft)

    def _find_draft_title(self, title):
        for i in self.draftLst:
            if i.title == title:
                return self.draftLst.index(i)
        return -1

    def list_draft(self):
        print("Drafts:")
        for i in self.draftLst:
            print(i.title)

    def send_draft(self, title):
        idx = self._find_draft_title(title)
        if idx != -1:
            self.draftLst[idx].send_draft(self.smtpObj)
            del self.draftLst[idx]

    def send_all_draft(self):
        for i in self.draftLst:
            i.send_draft(self.smtpObj)
        self.draftLst = []

    def _byte2str(self, data):
        if isinstance(data, bytes):
            try:
                data = data.decode()
            except UnicodeDecodeError:
                data = data.decode("gb2312", 'replace')
        return data

    def get_all_mail(self):
        self.imapObj.noop()
        status, msgs = self.imapObj.search(None, "ALL")
        msgs = msgs[0].split()

        pbar = tqdm(msgs)
        for mail_id in pbar:
            if mail_id in self.emailIDLst: continue
            status, msg = self.imapObj.fetch(mail_id, "(RFC822)")
            for responsePart in msg:
                if not isinstance(responsePart, tuple): continue
                emailMsg = email.message_from_bytes(responsePart[1])
                message = ""
                sender = emailMsg["From"]
                sender = decode_header(sender)[0][0]
                sender = self._byte2str(sender)
                title = emailMsg["Subject"]
                title = decode_header(title)[0][0]
                title = self._byte2str(title)

                if emailMsg.is_multipart():
                    # 处理多部分邮件
                    for part in emailMsg.walk():
                        content_type = part.get_content_type()
                        content_disposition = str(part.get("Content-Disposition"))
                        # 获取文本内容
                        if "text/plain" in content_type and "attachment" not in content_disposition:
                            message = part.get_payload(decode=True)
                        # TODO:
                        # 获取其他附件内容
                else:
                    # 非多部分邮件（纯文本邮件）
                    message = emailMsg.get_payload(decode=True)
                message = self._byte2str(message)

                emailObj = MailDraft(title=title, sender=sender, receivers=["2053232384@qq.com"])
                emailObj.add_msg(message)
                emailObj.id = mail_id
                self.emailLst.append(emailObj)
                self.emailIDLst.append(mail_id)
                self.unreadMailIDLst.append(emailObj)

    def list_email(self):
        print("Emails:")
        for i in self.emailLst:
            print(i.title)

    def logout(self):
        self.smtpObj.quit()
        self.imapObj.logout()


if __name__ == "__main__":
    new_draft = MailDraft(title="test", sender="2053232384@qq.com", receivers=["2997839760@qq.com"])
    mailbox = MailBox(host="smtp.qq.com", username="2053232384", pwd="syktappnjddlcadd")
    # new_draft.add_msg("I'm Zichuan Yang\nI'm 22 years old\nThis is a test mail for the print format of the mail draft. The next task is to combine email functions"
    #                   "and chat functions. Then, try to build a multi-tread architecture for this function.")
    # print(new_draft)
    # mailbox.list_draft()
    # mailbox.add_draft(new_draft)
    # mailbox.list_draft()
    # mailbox.send_all_draft()
    # mailbox.list_draft()

    mailbox.get_all_mail()
    mailbox.list_email()
    for i in mailbox.unreadMailIDLst:
        print(i)
