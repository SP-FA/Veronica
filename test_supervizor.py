import os
import sys

from utils.configure_util import CfgLoader
from vero_supervizor import ProcessAgentActions, SupervisorHost


if __name__ == "__main__":
    rootPath = sys.path[0]
    cfg = CfgLoader(os.path.join(rootPath, "cfg.yaml"))

    email_cfg = CfgLoader(os.path.join(rootPath, "vero_chat_agent/configs/vero_email.yaml")).params
    email_cfg = {
        "type": "email",
        "receivers": email_cfg["receivers"],
        "sender": email_cfg["sender"],
        "mail_params": {
            "mail_host": email_cfg["mail_host"],
            "mail_user": email_cfg["mail_user"],
            "mail_pass": email_cfg["mail_pass"],
        }
    }

    wechat_cfg = CfgLoader(os.path.join(rootPath, "vero_chat_agent/configs/vero_wechat.yaml")).params
    wechat_cfg = {
        "type": "wechat",
        "receivers": [wechat_cfg["wechat_default_receiver"]],
    }

    cfg.add(email_cfg=email_cfg, wechat_cfg=wechat_cfg)
    params = cfg.params

    host = SupervisorHost(params["port"], ProcessAgentActions(), params["email_cfg"])
