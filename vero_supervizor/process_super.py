import enum
import os
import psutil

from vero_visualizer.text_visualizer import TextVisualizer


class Timer(enum.Enum):
    TIMER_OFF = 0
    TIMER_ON = 1


class ProcState(enum.Enum):
    PROC_RESPONSE = 0
    PROC_FINISH = 1
    PROC_REGULAR = 2


class Supervisor:
    """实现一个监视器类，主要功能为：
    - 获取全部进程
    - TODO: 打印进程信息
    - 获取注册的进程信息（如果进程名中含有 '@'，则定义为 被注册，被注册的进程可以通过 Supervisor 获取个性化的信息）
        - 获取注册的进程
        - TODO: 获取个性化信息
        - TODO: 手动打印 / 完成时打印 / (定时打印)

    Attributes:
        user (str): 登录系统的用户名
        allProcess (List[Process]): 所有的进程
    """

    def __init__(self):
        """
        TODO: 原本需要在这里登录邮箱，但是应该将这一功能解耦所以目前 Supervisor 类不包括邮箱功能
        """
        self.user = os.getlogin()
        self.allProcess = []
        self.find_process()

    def find_process(self):
        """查找该账户的所有进程，"root" 用户查看所有进程

        Returns:
            Dict: 所有 process 的信息
                  格式为 {"pid":, "name":, "username", "exe", "cwd", "parents", "cfgPath":}
        """
        pids = psutil.pids()
        procs = []
        for pid in pids:
            proc = psutil.Process(pid)
            if self.user != proc.username() and self.user != "root": continue
            cfg = f"{proc.cwd()}/{proc.name()}.yaml"
            procInfo = {
                "pid": pid,
                "name": proc.name(),
                "username": proc.username(),
                "exe": proc.exe(),
                "cwd": proc.cwd(),
                "parents": proc.parents(),
                "cfgPath": cfg
            }
            procs.append(procInfo)
        self.allProcess = procs
        return procs

    def find_registered_process(self, procList=None):
        """从 procList 中找出注册过的进程

        Args:
            procList (List[Process]): 一个列表，每个元素是一个进程信息类

        Returns:
            Dict: 所有已注册的 process 的信息
                  格式为 {"pid":, "name":, "username", "exe", "cwd", "parents", "cfgPath":}
        """
        if procList is None:
            procList = self.allProcess

        procs = []
        for proc in procList:
            if "@" in proc["name"]:
                procs.append(proc)
        return procs

    def get_finished_process(self):
        current_process = self.find_process()
        terminate_process = list(filter(lambda x: x not in current_process, self.allProcess))
        self.allProcess = current_process
        return terminate_process

    def __str__(self):
        visualizer = TextVisualizer(80, "  |\n|  ")
        totalString = ""
        # for proc in self.allProcess:
            # pid = proc["pid"]
            # name = proc["name"]
            # username = proc["username"]
            # exe = proc["exe"]
            # cwd = proc["cwd"]
            # parents = proc["parents"]
