"""
Author: Zichuan Yang
Date: 2023-12-20
"""

import itchat
from itchat.content import TEXT
import time
from chat_model import Ernie


class ChatData:
    def __init__(self, name, model="ernie"):
        self._name = name
        self.data = {
            'messages': [
                {
                    'role': 'user',
                    'content': '你是谁？'
                },
                {
                    'role': 'assistant',
                    'content': '我是 Veronica，一位赛博管家。'
                }
            ]
        }
        if model == "ernie": self.ernie = Ernie()

    @property
    def name(self):
        return self._name

    def update_data(self, role, content):
        self.data["messages"].append({
            'role': role,
            'content': content
        })

    def gen_response(self):
        res = self.ernie.chat(self.data)
        self.update_data('assistant', res)
        return res


if __name__ == '__main__':
    itchat.auto_login(hotReload=True)  # hotReload=True 可以暂存登录状态，退出后一定时间内重启不用再次扫码登录
    time.sleep(1)
    chat = ChatModel()
    chatDict = {}

    @itchat.msg_register(TEXT)
    def friend_reply(msg):
        if msg.User["UserName"] == "filehelper": return
        print(f"{msg.User['UserName']} receive: ", msg.text)
        friendName = msg.User["UserName"]
        if friendName not in chatDict.keys():
            chatDict[friendName] = ChatData(friendName)
        chatDict[friendName].update_data('user', msg.text)
        res = chatDict[friendName].gen_response()
        print("send: ", res)
        itchat.send(res, toUserName=msg.User["UserName"])


    @itchat.msg_register(TEXT, isGroupChat = True)
    def group_reply(msg):
        if not msg['isAt']: return
        print(f"{msg.User['NickName']} receive: ", msg.text)
        groupName = msg.User["NickName"]
        if groupName not in chatDict.keys():
            chatDict[groupName] = ChatData(groupName)
        chatDict[groupName].update_data('user', msg.text)
        res = chatDict[groupName].gen_response()
        res = f"@{msg['ActualNickName']}\u2005 " + res
        print("send: ", res)
        itchat.send(res, toUserName=msg['FromUserName'])

    itchat.run()
