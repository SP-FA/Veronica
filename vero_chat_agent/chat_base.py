from vero_visualizer import DictVisualizer, TextVisualizer


class MessageDraft:
    """ 消息草稿基类 """
    LINE_LENGTH = len("=========================================================")
    
    def __init__(self, title, receivers, msg):
        self.title = title
        self.receivers = receivers
        self.msg = msg
        
        self.text_visual = TextVisualizer(self.LINE_LENGTH, beforeLine="|  ", afterLine="  |")
        self.dict_visual = DictVisualizer()

    def add_msg(self, newMsg):
        self.msg = self.msg + newMsg


class MessageTransceiver:
    """ 消息收发基类 """
    def __init__(self):
        self.draftLst = []

    def add_draft(self, draft):
        """ 添加草稿 """
        self.draftLst.append(draft)

    def send(self):
        """ 发送消息 """
        raise NotImplementedError

    def receive(self):
        """ 接收/检查新消息 """
        raise NotImplementedError

    def logout(self):
        """ 登出/断开连接 """
        raise NotImplementedError
