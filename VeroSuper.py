import psutil
import yaml
import os
from pyEmail import Mail
from threading import Timer


TIME_INTERVAL = 360 # 要改成可变的，不能写死
                    # 必要的话可以改成每个程序单独设置，监视器使用计数器来统计时间

TIMER_ON = 1
TIMER_OFF = 0

PROC_REGULAR = 0
PROC_FINISH = 1


def _gen_msg(conf, status):
    if status == PROC_FINISH:
        title = "[Fin][4070ti 计算节点] 任务 %s 已经完成" % (conf["title"])
    elif status == PROC_REGULAR:
        title = "[Reg][4070ti 计算节点] 任务 %s 定时汇报" % (conf["title"])

    msg = conf["message"] + "\n"
    if conf["epoch"] is not None:
        if conf["epoch"]["now"] is not None:
            msg = msg + "已完成 " + str(conf["epoch"]["now"]) + " epoch，"
        if conf["epoch"]["total"] is not None:
            msg = msg + "共 " + str(conf["epoch"]["total"]) + " epoch"
    return title, msg + "\n"


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

    def _send_mails(self, procs, isTimer):
        #
        # procs: [{"pid": pid, "name": name}, ]
        #
        for proc in procs:
            try:
                p = psutil.Process(proc["pid"])
                path = p.cwd() + "/" + proc["name"] + ".yaml"
            except psutil.NoSuchProcess:
                path = proc["cfg"]

            conf = rd_yaml(path)
            rcv = self.receivers.copy()
            try:
                rcv.append(conf["mailbox"])
            except (KeyError, TypeError):
                pass

            if isTimer == TIMER_ON and conf["timer"] == TIMER_ON:
                title, msg = _gen_msg(conf, PROC_REGULAR)
            elif isTimer == TIMER_OFF:
                title, msg = _gen_msg(conf, PROC_FINISH)
            else:
                continue

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
