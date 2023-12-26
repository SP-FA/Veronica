import time

from vero_email.py_email import MailBox, MailDraft
from chat import ChatModel


if __name__ == "__main__":
    mailbox = MailBox(host="smtp.qq.com", username="2053232384", pwd="syktappnjddlcadd")
    chat = ChatModel()
    mailbox.get_all_mail()
    mailbox.unreadMailIDLst = []
    while 1:
        time.sleep(5)
        mailbox.get_all_mail()
        if len(mailbox.unreadMailIDLst) > 0:
            draft = mailbox.unreadMailIDLst[0]
            print(draft)
            msg = draft.msg
            # chat.add_data('user', msg)
            # res = chat.chat()
            new_draft = MailDraft(title=draft.id, sender="2053232384@qq.com", receivers=["2997839760@qq.com"])
            new_draft.add_msg(res)
            mailbox.add_draft(new_draft)
            mailbox.send_all_draft()
            mailbox.unreadMailIDLst = []
