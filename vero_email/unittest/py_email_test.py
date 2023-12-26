import unittest

from utils.configure_util import ConfLoader
from vero_email.py_email import MailDraft, MailBox


class MyTestCase(unittest.TestCase):
    def test_print_mail(self):
        path = "../../conf.yaml"
        params = ConfLoader(path)
        sender = params.params["sender"]
        receiver = params.params["receiver"]

        draft = MailDraft(title="test", sender=sender, receivers=receiver)
        draft.add_msg("I'm Zichuan Yang\nI'm 22 years old\nThis is a test mail for the print format of the mail "
                      "draft. The next task is to combine email functions and chat functions. Then, try to build a "
                      "multi-tread architecture for this function.")
        print(draft)

    def test_send_mail(self):
        path = "../../conf.yaml"
        params = ConfLoader(path)
        sender = params.params["sender"]
        receiver = params.params["receiver"]

        draft = MailDraft(title="test", sender=sender, receivers=receiver)
        mailbox = MailBox(params)
        mailbox.add_draft(draft)
        mailbox.list_draft()
        mailbox.send_all_draft()

    def test_receive_mail(self):
        path = "../../conf.yaml"
        params = ConfLoader(path)

        mailbox = MailBox(params)
        mailbox.get_all_mail()
        mailbox.list_email()
        for i in mailbox.unreadMailIDLst:
            print(i)


if __name__ == '__main__':
    unittest.main()
