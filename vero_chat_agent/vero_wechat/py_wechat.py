import time
from collections import defaultdict

import itchat
from itchat.content import TEXT

from vero_chat_agent.chat_base import MessageTransceiver, MessageDraft


class WeChatDraft(MessageDraft):
    """ 用于维护一条微信消息 / 草稿"""
    def __init__(self, receivers, msg):
        super().__init__(receivers, msg)
    
    def __str__(self):
        r = self.text_visual(f"Receivers :")
        receivers = self.text_visual(self.receivers)
        content = self.text_visual(self.msg)
        return (
            f"=============================Draft=============================\n"
            f"{self.text_visual.blankLine}"
            f"{r}"
            f"{receivers}"
            f"{self.text_visual.blankLine}"
            f"{self.text_visual.splitLine}"
            f"{self.text_visual.blankLine}"
            f"{content}"
            f"===============================================================\n"
        )


class WeChat(MessageTransceiver):
    def __init__(self, hotReload=True):
        self.unreadLst = []
        self.receive_buffer = defaultdict(list)
        super().__init__()
        itchat.auto_login(hotReload=hotReload)
        time.sleep(1)
        # 注册回调
        @itchat.msg_register(TEXT)
        def _friend_reply(msg):
            return self._handle_msg(msg)

        @itchat.msg_register(TEXT, isGroupChat=True)
        def _group_reply(msg):
            return self._handle_group_msg(msg)

    def _handle_msg(self, msg):
        if msg.User["UserName"] == "filehelper": return
        print(f"{msg.User['UserName']} receive: ", msg.text)
        self.receive_buffer[msg.User["UserName"]] = msg.text

    def _handle_group_msg(self, msg):
        if not msg['isAt']: return
        print(f"{msg.User['NickName']} receive: ", msg.text)
        self.receive_buffer[msg.User["NickName"]].append(msg.text)

    def receive(self):
        """ 返回一个 dict, key 是发送者的 UserName 或 NickName, value 是消息内容 """
        for k, v in self.receive_buffer.items():
            for i in v:
                self.unreadLst.append(WeChatDraft([k], i))
        self.receive_buffer = defaultdict(list)

    def add_draft(self, draft):
        self.draftLst.append(draft)

    def send(self):
        """ target 为微信的 UserName 或 NickName """
        for i in self.draftLst:
            print(f"WeChat Send to {i.target}: {i.msg}")
            itchat.send(i.msg, toUserName=i.target)
        self.draftLst = []

    def logout(self):
        itchat.logout()
