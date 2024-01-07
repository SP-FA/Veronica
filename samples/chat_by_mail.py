import time

from utils.configure_util import ConfLoader
from vero_email.py_email import MailBox, MailDraft
from vero_chat.chat_model import ChatSession


if __name__ == "__main__":
    params = ConfLoader("../conf.yaml")
    mailbox = MailBox(params)
    chat = ChatSession("email_session")
    mailbox.get_all_mail()
    mailbox.unreadMailIDLst = []
    while 1:
        time.sleep(5)
        mailbox.get_all_mail()
        if len(mailbox.unreadMailIDLst) > 0:
            draft = mailbox.unreadMailIDLst[0]
            print(draft)
            msg = draft.msg
            res = chat.gen_response(msg)
            new_draft = MailDraft(title=draft.id, sender="2053232384@qq.com", receivers=["2997839760@qq.com"])
            new_draft.add_msg(res)
            mailbox.add_draft(new_draft)
            mailbox.send_all_draft()
            mailbox.unreadMailIDLst = []
