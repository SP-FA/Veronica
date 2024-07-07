"""
author: 2265288589@qq.com
date: 2024 / 4/ 19
"""

import requests
import json
import configparser

from vero_auto_sign.get_params import get_user_params
from utils.configure_util import ConfLoader
from vero_email.py_email import MailBox, MailDraft

GAME_DICT = {
    "genshin": "genshin_info",
    "starrail": "starrail_info"
}


def sign_request(url, headers, data):
    response = requests.post(url, headers=headers, data=json.dumps(data))
    responseData = response.text
    parseResponseData = json.loads(responseData)
    try:
        if parseResponseData["data"]["gt"] == "":
            return responseData
        else:
            challenge = parseResponseData['data']['challenge']
            headers['x-rpc-challenge'] = challenge
            response = requests.post(url, headers=headers, data=json.dumps(data))
            return response.text
    except:
        return responseData


def sign(cfgPath, gameName):
    try:
        cfg = configparser.ConfigParser()
        cfg.read(cfgPath)

        gameSection = GAME_DICT[gameName.lower()]
        uid = cfg[gameSection]['uid']
        hdid = cfg[gameSection]['hdid']
        region = cfg[gameSection]['region']
        dh = cfg[gameSection]['dh']

        url = cfg['api']['url']
        ltoken = cfg['params']['ltoken']
        mys_id = cfg['params']['aid']
        loginTicket = cfg['params']['login_ticket']
        cookieToken = cfg['params']['cookie_token']

        headers = {
            'x-rpc-signgame': dh,
            'Cookie':
                'login_ticket=' + loginTicket + ';' + \
                'account_id=' + mys_id + ';' + \
                'ltoken=' + ltoken + ';' + \
                'cookie_token=' + cookieToken + ';'
        }
        data = {
            "act_id": hdid,
            "region": region,
            "uid": uid,
            "lang": "zh-cn"
        }
        res = sign_request(url, headers, data)
        return res.split(",")[1].split("\"")[-2]
    except:
        return f"{cfgPath} is not available for game {gameName}"


if __name__ == "__main__":
    path = "../conf.yaml"
    params = ConfLoader(path)
    sender = params["sender"]
    receiver = params["receiver"]
    mailbox = MailBox(params)

    draft = MailDraft(title="[Auto] 原神签到报告", sender=sender, receivers=receiver, msg="今日签到结果：\n")
    cfgPath = "./cfgs/example.cfg"
    user = "SPFA"
    # users = ["example"]
    # for user in users:
    # get_user_params(cfgPath, "./public_key.pem")
    msg = sign(cfgPath, "starrail")
    draft.add_msg(f"- {user}: {msg}")

    print(draft)
    mailbox.add_draft(draft)
    mailbox.list_draft()
    # mailbox.send_all_draft()
