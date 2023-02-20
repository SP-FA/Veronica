#
# 1. 在需要被监视的代码内加入如下片段：
#   - 修改进程名称，添加特殊标识符以能被监视。
#   - 修改配置文件，包括了所有要通过邮件发送的结果
#
# 2. 监视器：
#   - 遍历进程队列
#   - 查看进程状态：
#       - 进程仍在运行
#           - 如果要求定时发生报告，则发送邮件
#       - 不在运行：将结果发送邮件
#           - 获取进程工作目录，找到配置文件
#
# 3. 自动化管理任务：
#   - 任务列表增删
#   - 任务排队执行
#   - 查看不同用户提交的任务
#
# 4. 远程监控电脑状态：
#   - 获取 CPU GPU 占用、温度等参数
#       - 在紧急情况下（占用率 100%，温度过高）
#       - 手动获取
#

import setproctitle
import psutil
from typing import *
import yaml
import os
from pyEmail import Mail
from threading import Timer


TIME_INTERVAL = 360

TIMER_ON = 1
TIMER_OFF = 0


#
# 当前 yaml 文件结构：
# title : str
# message : str
# imgPaths:
#   -
#     path : str
#     name : str
# filePaths:
#   -
#     path : str
#     name : str
# epoch:
#   now : int 当前迭代数量
#   total : int 总迭代数
# timer: int 是否启用定时，0 为不启用，1 为启用
# mailbox: str
#
def write_yaml(title, msg=None, imgPaths=None, filePaths=None, epoch=None, timer=TIMER_OFF, mailbox=""):
    #
    # imgPaths = [{"path": path, "name": file name}]
    # epoch = {"now": , "total": }
    #
    path = os.getcwd() + "/" + title + ".yaml"
    with open(path, 'w', encoding='utf-8') as f:
        dct = {"title": title}
        if msg is not None:
            dct.update({"message": msg})

        if imgPaths is not None:
            dct.update({"imgPaths": imgPaths})

        if filePaths is not None:
            dct.update({"filePaths": filePaths})

        if epoch is not None:
            dct.update({"epoch": epoch})

        if timer != 0 and timer != 1:
            timer = 0
        dct.update({"timer": timer})

        if mailbox != "":
            dct.update({"mailbox": mailbox})

        yaml.dump(dct, stream=f, allow_unicode=True)


def read_yaml(path):
    with open(path, 'r', encoding='utf-8') as f:
        dct = yaml.load(f.read(), Loader=yaml.FullLoader)
    return dct


def change_yaml(path, dct, node: str):
    config = read_yaml(path)
    config[node] = dct
    with open(path, 'w', encoding='utf-8') as f:
        yaml.dump(config, stream=f, allow_unicode=True)


def _gen_fin_msg(conf):
    msg = "[Due][4070ti 计算节点] 任务 %s 已经完成\n" % (conf["title"])
    msg = msg + conf["message"] + "\n"
    if conf["epoch"] is not None:
        if conf["epoch"]["now"] is not None:
            msg = msg + "已完成 " + str(conf["epoch"]["now"]) + " epoch，"
        if conf["epoch"]["total"] is not None:
            msg = msg + "共 " + str(conf["epoch"]["total"]) + " epoch"
    return msg + "\n"


def _gen_tmr_msg(conf):
    msg = "[Reminder][4070ti 计算节点] 任务 %s 定时汇报\n" % (conf["title"])
    msg = msg + conf["message"] + "\n"
    if conf["epoch"] is not None:
        if conf["epoch"]["now"] is not None:
            msg = msg + "已完成 " + str(conf["epoch"]["now"]) + " epoch，"
        if conf["epoch"]["total"] is not None:
            msg = msg + "共 " + str(conf["epoch"]["total"]) + " epoch"
    return msg + "\n"


class SetProcess:
    def __init__(self, title):
        self.title = os.getlogin() + "@" + title
        setproctitle.setproctitle(self.title)

        pids = psutil.pids()
        for pid in pids:
            proc = psutil.Process(pid)
            if "super@super" in proc.name():
                return
        os.system("bash /home/yzc/Veronica/startSuper.sh")

    def configer(self, msg=None, imgPaths: List = None, filePaths: List = None, timer=TIMER_OFF, mailbox=""):
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

        write_yaml(self.title, msg, imgPaths, filePaths, timer, mailbox)

    def set_epoch(self, now, total):
        e = {"now": now, "total": total}
        change_yaml(os.getcwd() + "/" + self.title + ".yaml", e, "epoch")

    #
    # TODO: 允许增加 msg 图片 文件 路径
    #


class Supervisor:
    def __init__(self):
        self.user = os.getlogin()
        self.procL = []

        mail_host = 'smtp.qq.com'
        mail_user = '2053232384'
        mail_pass = 'syktappnjddlcadd'
        self.sender = '2053232384@qq.com'
        # receivers 需要设置，用户提前对用户名绑定邮箱
        self.receivers = ['2997839760@qq.com']
        self.email = Mail(mail_host, mail_user, mail_pass)

    def _find_process(self):
        #
        # procs: {"pid":, "name":, "cfg":}
        #
        pids = psutil.pids()
        procs = []
        for pid in pids:
            proc = psutil.Process(pid)
            if self.user == "root" and "@" in proc.name():
                cfg = proc.cwd() + "/" + proc.name() + ".yaml"
                procs.append({"pid": pid, "name": proc.name(), "cfg": cfg})
            elif self.user != "root":
                if self.user + "@" in proc.name():
                    cfg = proc.cwd() + "/" + proc.name() + ".yaml"
                    procs.append({"pid": pid, "name": proc.name(), "cfg": cfg})
        return procs

    def _get_fin_process(self):
        procI = self._find_process()

        procA = list(filter(lambda x: x not in self.procL, procI))
        self.procL.extend(procA)

        termL = list(filter(lambda x: x not in procI, self.procL))
        self.procL = list(filter(lambda x: x not in termL, self.procL))
        return termL

    def _send_mails(self, procs, isTimer: int):
        #
        # procs: [{"pid": pid, "name": name}, ]
        #
        for proc in procs:
            try:
                p = psutil.Process(proc["pid"])
                path = p.cwd() + "/" + proc["name"] + ".yaml"
            except psutil.NoSuchProcess:
                path = proc["cfg"]

            conf = read_yaml(path)
            rcv = self.receivers.copy()
            try:
                rcv.append(conf["mailbox"])
            except KeyError:
                pass

            title = "维罗妮卡工作报告：关于 " + conf["title"]

            msg = ""
            if isTimer == TIMER_ON and conf["timer"] == TIMER_ON:
                msg = _gen_tmr_msg(conf)
            elif isTimer == TIMER_OFF:
                msg = _gen_fin_msg(conf)

            self.email.create_mail(title, self.sender, rcv)
            self.email.add_msg(title, msg)
            self.email.add_img(title, conf["imgPaths"])
            self.email.add_file(title, conf["filePaths"])
        self.email.send_all()

    def _timer_func(self, num):
        procs = self._get_fin_process()
        if procs:
            self._send_mails(procs, TIMER_OFF)
        if num > 1:
            num -= 1
        else:
            num = TIME_INTERVAL
            self._send_mails(self._find_process(), TIMER_ON)
        timer = Timer(10, self._timer_func, (num,))
        timer.start()

    def supervise(self):
        timer = Timer(10, self._timer_func, (TIME_INTERVAL,))
        timer.start()
