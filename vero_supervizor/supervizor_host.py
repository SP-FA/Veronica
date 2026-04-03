import socket
import json
import threading

from vero_supervizor.supervisor_enum import ProcState
from vero_supervizor.supervisor_proc_agent import ProcessAgent, ProcessAgentActions

lock = threading.Lock()  # 防止多线程写冲突


class SupervisorHost:
    """维护一个监控进程的主机信息
    """
    def __init__(self, port: int, actions: ProcessAgentActions):
        self.host = '127.0.0.1'
        self.port = port
        self.proccesses = {}  # 监控的进程列表，key 为进程名称，value 为进程
        self.actions = actions

        t = threading.Thread(target=self.start_listen, daemon=True)
        t.start()

    def start_listen(self):
        """启动主机，监听端口并处理客户端连接
        """
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((self.host, self.port))
            s.listen()
            print(f"Listening on {self.host}:{self.port}")

            while True:
                conn, addr = s.accept()

                # 每个客户端一个线程
                t = threading.Thread(
                    target=self._handle_client,
                    args=(conn, addr),
                    daemon=True
                )
                t.start()
    
    def _handle_client(self,conn, addr):
        print("Connected:", addr)
        buffer = b''
        try:
            while True:
                data = conn.recv(4096)
                if not data: break

                buffer += data
                while True:
                    if len(buffer) < 4: break

                    length = int.from_bytes(buffer[:4], 'big')
                    if len(buffer) < 4 + length: break

                    msg = buffer[4:4+length]
                    buffer = buffer[4+length:]
                    try:
                        decoded = json.loads(msg.decode('utf-8'))
                        print(f"[{addr}] Received:", decoded)
                        self.handle_msg(decoded)

                    except Exception as e:
                        print("Decode error:", e)
        finally:
            conn.close()
            print("Disconnected:", addr)

    def handle_msg(self, msg: dict):
        """处理客户端发送的消息

        Args:
            msg (dict): 客户端发送的消息，包含监控数据，格式为：{
                "task": "register" / "update" / "finish",
                "proc_name": "process1",
                "report_condition": ReportCondition,
                "data": {...}
            }
        """
        task = msg.get("task", "unknown")  # 任务标识
        proc_name = msg.get("proc_name", "unknown")
        if task == "register":
            report_condition = msg.get("report_condition", {})
            actions = msg.get("actions", self.actions)
            self.proccesses[proc_name] = ProcessAgent(proc_name, report_condition, actions)
        elif task == "update":
            data = msg.get("data", {})
            self.proccesses[proc_name].update(data)
        elif task == "finish":
            self.proccesses[proc_name].finish()
        else:
            print("Unknown task:", task)

