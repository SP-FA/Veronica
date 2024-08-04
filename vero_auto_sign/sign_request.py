"""
author: 2265288589@qq.com
date: 2024 / 4/ 19
"""

import requests
import json
import configparser

from vero_email.py_email import MailBox, MailDraft

GAME_DICT = {
    "genshin": "genshin_info",
    "starrail": "starrail_info",
    "zzz": "zzz_info",
}


def sign_request(url: str, headers: dict, data: dict) -> str:
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


def sign(cfgPath: str, gameName: str) -> str:
    try:
        cfg = configparser.ConfigParser()
        cfg.read(cfgPath)
    except:
        raise f"{cfgPath} is not available for game {gameName}"

    gameSection = GAME_DICT[gameName.lower()]
    uid = cfg[gameSection]['uid']
    hdid = cfg[gameSection]['hdid']
    region = cfg[gameSection]['region']
    dh = cfg[gameSection]['dh']

    if gameName == "zzz":
        url = cfg['api']['url-zzz']
    else:
        url = cfg['api']['url']

    ltoken = cfg['params']['ltoken']
    mys_id = cfg['params']['aid']
    loginTicket = cfg['params']['login_ticket']
    cookieToken = cfg['params']['cookie_token']

    headers = {
        'x-rpc-signgame': dh,
        'Cookie': f"login_ticket={loginTicket};account_id={mys_id};ltoken={ltoken};cookie_token={cookieToken};",
    }
    data = {
        "act_id": hdid,
        "region": region,
        "uid": uid,
        "lang": "zh-cn",
    }
    res = sign_request(url, headers, data)
    return res.split(",")[1].split("\"")[-2]


def sign_process(user, cfgPath, params):
    sender = params["sender"]
    receiver = params["receiver"]
    mailbox = MailBox(params)

    draft = MailDraft(title="[Auto] 原神签到报告", sender=sender, receivers=receiver, msg="今日签到结果：\n")
    # users = ["example"]
    # for user in users:
    # get_user_params(cfgPath, "./public_key.pem")
    msg = sign(cfgPath, "genshin")
    draft.add_msg(f"- [genshin] {user}: {msg}\n")
    msg = sign(cfgPath, "starrail")
    draft.add_msg(f"- [starrail] {user}: {msg}\n")
    msg = sign(cfgPath, "zzz")
    draft.add_msg(f"- [zzz] {user}: {msg}\n")

    print(draft)
    mailbox.add_draft(draft)
    mailbox.list_draft()
    mailbox.send_all_draft()
