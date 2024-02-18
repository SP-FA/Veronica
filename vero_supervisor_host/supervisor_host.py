# 用于探索使用 socket 方式实现 supervisor
# 这个是 host 端，用于读取 Linux 指定文件夹下的 socket 文件
# client 文件应包括一个 json，包含了这个进程的所需信息
import os
import socket


class Timer:
    TIMER_OFF = 0
    TIMER_ON = 1


class ProcReportCondition:
    """表示进程报告条件的枚举

    Attributes:
        RESPONSE: 只有在询问时报告该进程状态
        FINISH (default): 在进程结束时报告该进程状态，在询问时也可以进行报告
        REGULAR: 每过一段时间报告该进程状态，在进程终止或者询问时也可以进行报告
    """
    RESPONSE = 0
    FINISH = 1
    REGULAR = 2


class ProcState:
    """表示进程状态的枚举

    Attributes:
        PROC_PROCESSING: 进程正在运行
        PROC_FINISH: 进程终止
    """
    PROC_PROCESSING = 0
    PROC_FINISH = 1


class Socket:
    ########
    # 存在一个进程池去维护所有的 proc， e.g. [proc1, proc2, proc3]
    # proc 信息由客户端发送
    ########

    BUFFER_LENGTH = 1024

    def __init__(self, serverAddress="/home/yzc/vero_supervisor_server.sock"):
        try:
            os.unlink(serverAddress)
        except OSError:
            if os.path.exists(serverAddress): raise

        self.serverSocket = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        self.serverSocket.bind(self.serverAddress)
        self.serverSocket.listen(1)

    def run_socket(self):
        while True:
            print("class Socket 正在等待连接。。。")
            connection, clientAddress = self.serverSocket.accept()
            print(f"连接来自{clientAddress}")
            data = connection.recv(self.BUFFER_LENGTH)
            print(f"收到消息{data.decode()}")
            connection.close()


class Supervisor:
    def __init__(self, useTimer=Timer.TIMER_OFF, timeInterval=None):
        self.useTimer = useTimer
        self.timeInterval = timeInterval

    def set_timer(self, useTimer, timeInterval=None):
        """设置定时器

        Args:
            useTimer (Timer): 一个枚举类型，可以为 Timer.TIMER_ON / Timer.TIMER_OFF
            timeInterval (int): 定时器时间周期，只有在 useTimer = Timer.TIMER_ON 时生效
        """
        ######
        # 停止所有线程
        ######
        self.useTimer = useTimer
        if timeInterval is not None and useTimer == Timer.TIMER_ON:
            self.timeInterval = timeInterval
        ######
        # 重启所有线程（self.run()）
        ######

    def run(self):
        """启动监控程序
        1。 如果 self.useTimer == Timer.TIMER_ON，则启动定时器
        2. 如果某进程原本状态为 ProcState.PROC_REGULAR，但是现在状态为 ProcState.PROC_FINISH，则发送报告
        """

    def timer(self):
        """设置定时器，以后可能改成单独的类
        定时器的作用是定时发送所有进程状态为 ProcState.PROC_REGULAR 的进程信息
        """
