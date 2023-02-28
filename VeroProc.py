import yaml
import os
import setproctitle
import psutil


TIMER_OFF = 0


class SetProcess:
    def __init__(self, title):
        self.title = os.getlogin() + "@" + title
        setproctitle.setproctitle(self.title)

        self.ypath = os.getcwd() + "/" + self.title + ".yaml"

        pids = psutil.pids()
        for pid in pids:
            proc = psutil.Process(pid)
            if "super@super" in proc.name():
                return
        os.system("bash /home/yzc/Veronica/startSuper.sh")

    def configer(self, msg=None, imgPaths = None, filePaths = None, timer=TIMER_OFF, mailbox=""):
        #
        # @ imgPath: 存放 img 文件的文件夹所在的路径 / img 路径
        # @ filePath: 存放 file 文件的文件夹所在的路径 / file 路径
        #
        # Todo: 检查每个路径，将文件夹下的所需文件路径写入 yaml
        #
        for imgPath in imgPaths:
            path = imgPath["path"]
            path = os.path.abspath(path)
            imgPath["path"] = path

        for filePath in filePaths:
            path = filePath["path"]
            path = os.path.abspath(path)
            filePath["path"] = path

        wt_yaml(self.title, msg, imgPaths, filePaths, timer, mailbox)

    def set_epoch(self, now, total):
        e = {"now": now, "total": total}
        ch_yaml(self.ypath, e, "epoch")

    def change_node(self, dct, node):
        # TODO: 验证 node 是否允许 change
        ch_yaml(self.ypath, dct, node)

    def add_node(self, dct, node):
        # TODO: 验证 node 是否允许 add
        ad_yaml(self.ypath, dct, node)
