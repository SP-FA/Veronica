import itchat
from itchat.content import TEXT
import time
from vero_chat.chat_model import ChatSession


if __name__ == '__main__':
    itchat.auto_login(hotReload=True)  # , enableCmdQR=2 hotReload=True 可以暂存登录状态，退出后一定时间内重启不用再次扫码登录
    time.sleep(1)
    chatDict = {}

    @itchat.msg_register(TEXT)
    def friend_reply(msg):
        if msg.User["UserName"] == "filehelper": return
        print(f"{msg.User['UserName']} receive: ", msg.text)
        friendName = msg.User["UserName"]
        if friendName not in chatDict.keys():
            chatDict[friendName] = ChatSession(friendName)
        res = chatDict[friendName].gen_response(msg.text)
        print("send: ", res)
        itchat.send(res, toUserName=msg.User["UserName"])

    @itchat.msg_register(TEXT, isGroupChat=True)
    def group_reply(msg):
        if not msg['isAt']: return
        print(f"{msg.User['NickName']} receive: ", msg.text)
        groupName = msg.User["NickName"]
        if groupName not in chatDict.keys():
            chatDict[groupName] = ChatSession(groupName)
        res = chatDict[groupName].gen_response(msg.text)
        res = f"@{msg['ActualNickName']}\u2005 " + res
        print("send: ", res)
        itchat.send(res, toUserName=msg['FromUserName'])

    itchat.run()
