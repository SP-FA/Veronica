from vero_visualizer.dict_visualizer import DictVisualizer, TextVisualizer


class MessageDraft:
    """ 消息草稿基类 """
    LINE_LENGTH = len("=========================================================")
    
    def __init__(self, receivers, msg):
        self.receivers = receivers
        self.msg = msg
        
        self.text_visual = TextVisualizer(self.LINE_LENGTH, beforeLine="|  ", afterLine="  |")
        self.dict_visual = DictVisualizer()


class MessageTransceiver:
    """ 消息收发基类 """
    def __init__(self):
        self.draftLst = []

    def add_draft(self, draft):
        """ 添加草稿 """
        raise NotImplementedError

    def send(self):
        """ 发送消息 """
        raise NotImplementedError

    def receive(self):
        """ 接收/检查新消息 """
        raise NotImplementedError

    def logout(self):
        """ 登出/断开连接 """
        raise NotImplementedError
