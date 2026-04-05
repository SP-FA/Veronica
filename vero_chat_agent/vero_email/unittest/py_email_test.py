import sys
from pathlib import Path
_repo_root = Path(__file__).resolve().parents[3]  # unittest -> vero_email -> vero_chat_agent -> Veronica
sys.path.insert(0, str(_repo_root))

import os
import unittest

from utils import CfgLoader, VERO_EMAIL_LOG_DIR, VERO_EMAIL_CFG_PATH, REPO_ROOT, get_logger
from vero_chat_agent import MailDraft, MailBox

logger = get_logger(
    __name__,
    VERO_EMAIL_LOG_DIR,
    log_filename="vero_email_unittest.log",
)


class MyTestCase(unittest.TestCase):

    def _get_params(self):
        cfg = CfgLoader(os.path.join(REPO_ROOT, "cfg.yaml"))
        email_cfg = CfgLoader(VERO_EMAIL_CFG_PATH).params
        cfg.add(email_cfg=email_cfg)
        return cfg.params
        
    def test_print_mail(self):
        params = self._get_params()
        sender = params["email_cfg"]["sender"]
        receivers = params["email_cfg"]["receivers"]

        draft = MailDraft(title="test", sender=sender, receivers=receivers)
        draft.add_msg("I'm Zichuan Yang\nI'm 22 years old\nThis is a test mail for the print format of the mail "
                      "draft. The next task is to combine email functions and chat functions. Then, try to build a "
                      "multi-tread architecture for this function.")
        logger.info("%s", draft)

    # def test_send_mail(self):
    #     params = self._get_params()
    #     sender = params["email_cfg"]["sender"]
    #     receivers = params["email_cfg"]["receivers"]

    #     draft = MailDraft(title="test", sender=sender, receivers=receivers)
    #     mailbox = MailBox(params["email_cfg"])
    #     mailbox.add_draft(draft)
    #     mailbox.list_draft()
    #     mailbox.send()
    #     mailbox.logout()

    # def test_receive_mail(self):
    #     params = self._get_params()

    #     mailbox = MailBox(params["email_cfg"])
    #     mailbox.receive()
    #     mailbox.list_email()
    #     for i in mailbox.unreadMailIDLst:
    #         logger.info("%s", i)


if __name__ == '__main__':
    unittest.main()
