"""
author: 2265288589@qq.com
date: 2024 / 4/ 19
"""

import requests
import json
import configparser

from vero_auto_sign.encode_account_pwd import get_encode


def HQtokenAlogin_ticket(account, pwd):
    url = "https://passport-api.mihoyo.com/account/ma-cn-passport/app/loginByPassword"
    headers = {
        'Accept': '*/*',
        'x-rpc-app_id': 'bll8iq97cem8',
        'x-rpc-client_type': '1',
        'x-rpc-device_id': '2E632B19-A0B9-4723-8091-7460BD735144',
        'x-rpc-device_fp': '38d7f1f01547b',
        'x-rpc-device_name': 'iPhone',
        'x-rpc-device_model': 'iPhone14,4',
        'x-rpc-sys_version': '17.4.1',
        'x-rpc-game_biz': 'bbs_cn',
        'x-rpc-app_version': '2.70.1',
        'x-rpc-sdk_version': '2.20.1',
        'x-rpc-lifecycle_id': '1B062AAB-9685-4C97-B57B-A23DD86021D6',
        'x-rpc-account_version': '2.20.1',
        'Host': 'passport-api.mihoyo.com',
        'Accept-Encoding': 'gzip, deflate, br',
        'User-Agent': 'Hyperion/445 CFNetwork/1494.0.7 Darwin/23.4.0'
    }
    json_data = {
        "account": account,
        "password": pwd
    }

    response = requests.post(url, headers=headers, json=json_data)
    data = response.text
    parsed_data = json.loads(data)

    token = parsed_data['data']['token']['token']
    mid = parsed_data['data']['user_info']['mid']
    login_ticket = parsed_data['data']['login_ticket']
    aid = parsed_data['data']['user_info']['aid']
    return token, mid, login_ticket, aid


def HQcookie_token(token, mid):
    url1 = "https://passport-api.mihoyo.com/account/auth/api/getCookieAccountInfoBySToken"
    url2 = 'https://passport-api.mihoyo.com/account/auth/api/getLTokenBySToken'
    headers = {
        'Accept': '*/*',
        'Cookie': 'stoken=' + token + ';mid=' + mid,
        'Content-Type': 'application/json',
        'x-rpc-app_id': 'bll8iq97cem8',
        'x-rpc-client_type': '1',
        'x-rpc-device_id': '2E632B19-A0B9-4723-8091-7460BD735144',
        'x-rpc-device_fp': '38d7f1f01547b',
        'x-rpc-device_name': 'iPhone',
        'x-rpc-device_model': 'iPhone14,4',
        'x-rpc-sys_version': '17.4.1',
        'x-rpc-game_biz': 'bbs_cn',
        'x-rpc-app_version': '2.70.1',
        'x-rpc-sdk_version': '2.20.1',
        'x-rpc-lifecycle_id': '1B062AAB-9685-4C97-B57B-A23DD86021D6',
        'x-rpc-account_version': '2.20.1',
        'Host': 'passport-api.mihoyo.com',
        'Accept-Encoding': 'gzip, deflate, br',
        'User-Agent': 'Hyperion/445 CFNetwork/1494.0.7 Darwin/23.4.0'
    }

    response = requests.get(url1, headers=headers)
    data = response.text
    parsed_data = json.loads(data)
    cookie_token = parsed_data['data']['cookie_token']
    response = requests.get(url2, headers=headers)
    data = response.text
    parsed_data = json.loads(data)
    ltoken = parsed_data['data']['ltoken']
    return cookie_token, ltoken


def get_user_params(userCfgPath, pemPath):
    canshu = {}
    config = configparser.ConfigParser()
    config.read(userCfgPath)
    try:
        account = config['credentials']['account']
        password = config['credentials']['password']
        assert account != ''
        assert password != ''
    except:
        config = get_encode(pemPath, config)
        account = config['credentials']['account']
        password = config['credentials']['password']

    ticket = HQtokenAlogin_ticket(account, password)
    canshu['token'] = ticket[0]
    canshu['mid'] = ticket[1]
    canshu['login_ticket'] = ticket[2]
    canshu['aid'] = ticket[3]

    token = HQcookie_token(ticket[0], ticket[1])
    canshu['cookie_token'] = token[0]
    canshu['ltoken'] = token[1]

    for key, value in canshu.items():
        config.set('params', key, value)
    with open(userCfgPath, 'w') as configFile:
        config.write(configFile)


if __name__ == "__main__":
    get_user_params("./cfgs/SPFA.cfg", "./public_key.pem")


