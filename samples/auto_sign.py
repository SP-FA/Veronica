import os

os.chdir(os.path.dirname(__file__))

import time

from vero_auto_sign.get_params import get_user_params
from vero_auto_sign.sign_request import sign
from utils.configure_util import ConfLoader
from vero_email.py_email import MailBox, MailDraft

if __name__ == "__main__":
    params = ConfLoader("../conf.yaml")
    mailbox = MailBox(params)

    sender = params["sender"]
    receiver = params["receiver"]
    draft = MailDraft(title="[Auto] 米哈游签到报告", sender=sender, receivers=receiver)
    zzj_draft = MailDraft(title="米哈游签到", sender=sender, receivers=["2353968380@qq.com"])

    pemPath = "./vero_auto_sign/public_key.pem"
    userList = {
        "SPFA": "./vero_auto_sign/cfgs/SPFA.cfg",
        "momo": "./vero_auto_sign/cfgs/momo.cfg",
        "wfzzj": "./vero_auto_sign/cfgs/wfzzj.cfg"
    }

    for userName, cfgPath in userList.items():
        get_user_params(cfgPath, pemPath)
        time.sleep(60)

    draft.add_msg(f"Genshin Impact:\n")
    for userName, cfgPath in userList.items():
        msg = sign(cfgPath, "genshin")
        draft.add_msg(f"- {userName}: {msg}\n")
        time.sleep(1)

    draft.add_msg(f"\n\nStar Rail:\n")
    for userName, cfgPath in userList.items():
        msg = sign(cfgPath, "starrail")
        draft.add_msg(f"- {userName}: {msg}\n")
        if userName == "wfzzj":
            zzj_draft.add_msg(msg)
        time.sleep(1)

    mailbox.add_draft(draft)
    mailbox.add_draft(zzj_draft)
    mailbox.send_all_draft()
