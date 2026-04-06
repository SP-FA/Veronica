import socket
import json
import threading

from vero_supervizor import ReportCondition, TaskType, ProcessAgent, ProcessAgentActions
from utils import VERO_SUPERVISOR_LOG_DIR, get_logger

logger = get_logger(__name__, VERO_SUPERVISOR_LOG_DIR, log_filename="supervisor_host.log")


class SupervisorHost:
    """维护一个监控进程的主机信息
    """
    def __init__(self, port: int, actions: ProcessAgentActions, message_cfg: dict):
        """初始化主机，启动监听线程
        
        Args:
            port (int): 监听端口
            actions (ProcessAgentActions): 进程代理的可用操作
            message_cfg (dict): 消息配置，包含消息发送方式等信息，格式为：{
                "type": "email" / "wechat", 消息类型，用于指定报告的发送方式,
                "receivers": list, 接收者列表,
                "sender": str, 发送者（仅邮件类型需要）,
                "mail_params": dict, 邮件发送参数（仅邮件类型需要），格式为 {
                    "mail_host": str, SMTP 服务器地址,
                    "mail_user": str, 邮箱用户名,
                    "mail_pass": str, 邮箱密码,
                }
            }
        """
        self.host = '0.0.0.0'
        self.port = port
        self.processes = {}  # 监控的进程列表，key 为进程名称，value 为进程
        self.actions = actions
        self.message_cfg = message_cfg
        self.running = True

        self.processes_lock = threading.Lock()
        self.transceiver_lock = threading.Lock()

        if self.message_cfg["type"] == "email":
            from vero_chat_agent import MailBox
            self.message_transceiver = MailBox(self.message_cfg["mail_params"])
        elif self.message_cfg["type"] == "wechat":
            from vero_chat_agent import WeChat
            self.message_transceiver = WeChat()

        t = threading.Thread(target=self.start_listen, daemon=True)
        t.start()

    def start_listen(self):
        """启动主机，监听端口并处理客户端连接
        """
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((self.host, self.port))
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.listen()
            logger.info("Supervisor host listening on %s:%s", self.host, self.port)

            while self.running:
                conn, addr = s.accept()

                # 每个客户端一个线程
                t = threading.Thread(
                    target=self._handle_client,
                    args=(conn, addr),
                    daemon=True
                )
                t.start()
    
    def _handle_client(self,conn, addr):
        logger.info("Connected: %s", addr)
        buffer = b''
        try:
            while self.running:
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
                        logger.info("[%s] Received: %s", addr, decoded)
                        self.handle_msg(decoded)

                    except Exception as e:
                        logger.error("Decode error: %s", e)
        finally:
            conn.close()
            logger.info("Supervisor host disconnected: %s", addr)

    def close(self):
        """停止主机监听和处理客户端"""
        self.running = False
        logger.info("Supervisor host closed")

    def handle_msg(self, msg: dict):
        """处理客户端发送的消息

        Args:
            msg (dict): 客户端发送的消息，包含监控数据，格式为：{
                "task": "register" / "update" / "finish",
                "proc_name": "process1",
                "report_condition": ReportCondition 对象,
                "data": {...}
            }
        """
        task = msg.get("task", "unknown")  # 任务标识
        proc_name = msg.get("proc_name", "unknown")

        with self.processes_lock:
            if task == TaskType.REGISTER:
                report_condition = msg.get("report_condition", ReportCondition({}))
                actions = msg.get("actions") or ProcessAgentActions(self.actions.custom_actions)
                self.processes[proc_name] = ProcessAgent(proc_name, report_condition, actions, self.message_cfg)
                return
            agent = self.processes.get(proc_name)
        if not agent:
            logger.error("Unknown process: %s", proc_name)
            return
        
        draft = None
        if   task == TaskType.UPDATE: draft = agent.update(msg.get("data", {}))
        elif task == TaskType.FINISH: draft = agent.finish()
        else: logger.error("Unknown task: %s", task)
        
        if draft is None: return
        with self.transceiver_lock:
            self.message_transceiver.add_draft(draft)
            self.message_transceiver.send()

