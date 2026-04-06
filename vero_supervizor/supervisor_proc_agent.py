import copy
import threading

from vero_supervizor import ProcState
from vero_chat_agent import MessageDraft, MailDraft, WeChatDraft
from utils import VERO_SUPERVISOR_LOG_DIR, get_logger

logger = get_logger(__name__, VERO_SUPERVISOR_LOG_DIR, log_filename="supervisor_proc_agent.log")


class ProcessAgentActions:
    """表示一个被监控的进程的可用操作
    """
    def __init__(self, custom_actions: dict=None):
        """
        Args:
            agent (ProcessAgent): 关联的进程代理
            custom_actions (dict): 自定义操作列表，格式为：{
                "init": [{"name": "操作1", "description": "操作1的描述", "func": function}],
                "update": [{"name": "操作2", "description": "操作2的描述", "func": function}],
                "finish": [{"name": "操作3", "description": "操作3的描述", "func": function}],
                "regular": [{"name": "操作4", "description": "操作4的描述", "func": function}],
                "response": [{"name": "操作5", "description": "操作5的描述", "func": function}],
            }
        """
        self.agent = None  # 在进程注册时设置
        self.custom_actions = custom_actions
    
    def run_custom_action(self, task: str):
        res = []
        if self.custom_actions is None: return res
        for action in self.custom_actions.get(task, []):
            logger.info("Executing %s action: %s - %s", task, action["name"], action["description"])
            try:
                res.append(action["func"](self.agent))
            except Exception as e:
                logger.error("Error occurred while executing %s action: %s", task, e)
        return res

    def init_action(self, agent) -> list:
        """在进程注册时执行的操作
        """
        self.agent = agent
        res = self.run_custom_action("init")
        return res
    
    def response_action(self):
        """在询问时执行的操作

        TODO: 可以在这里添加一些默认的询问操作，比如生成当前进程状态的摘要、分析当前监控数据等
        """
        res = self.run_custom_action("response")
        return res

    def regular_action(self):
        """定期执行的操作

        TODO: 可以在这里添加一些默认的定期操作，比如检查进程状态、收集监控数据等
        """
        res = self.run_custom_action("regular")
        return res

    def update_action(self):
        """在进程状态更新时执行的操作
        """
        data = self.agent.latest_data
        if data is None: return

        data_str = "\n".join([f"{k}: {v}" for k, v in data.items()])
        res = [data_str]
        res.extend(self.run_custom_action("update"))
        return res

    def finish_action(self):
        """在进程完成时执行的操作
        """
        data = self.agent.latest_data
        if data is None: return

        data_str = "\n".join([f"{k}: {v}" for k, v in data.items()])
        res = [data_str]
        res.extend(self.run_custom_action("finish"))
        return res


class ProcessAgent:
    """表示一个被监控的进程
    """
    def __init__(self, name: str, report_condition: dict, actions: ProcessAgentActions, draft_cfg: dict):
        """
        Args:
            name (str): 进程名称
            report_condition (dict): 报告条件，格式为：{
                "RESPONESE": bool,  # 是否在询问时生成报告
                "REGULAR": bool,    # 是否定期生成报告
                "UPDATE": bool,     # 是否在状态更新时生成报告
                "FINISH": bool,     # 是否在进程完成时生成报告
            }
            actions (ProcessAgentActions): 关联的操作列表
            draft_cfg (dict): draft 配置信息，格式为: {
                "type": "email" / "wechat", 消息类型，用于指定报告的发送方式,
                "receivers": list, 接收者列表,
                "sender": str, 发送者（仅邮件类型需要）,
            }
        """
        self.name = name
        self.report_condition = report_condition
        self.actions = copy.deepcopy(actions)
        self.draft_cfg = draft_cfg
        self.state = ProcState.PROC_PROCESSING
        self._datas = []  # 存储该进程的监控数据

        self.lock = threading.Lock()

        self.actions.init_action(self)
    
    @property
    def latest_data(self):
        """返回最新的监控数据
        """
        if not self._datas or not len(self._datas): return None
        return self._datas[-1]
    
    def create_draft(self, title="", msg="") -> MessageDraft:
        """根据 message_type 创建对应类型的 MessageDraft
        """
        draft = None
        if self.draft_cfg["type"] == "email":
            draft = MailDraft(title, self.draft_cfg["sender"], self.draft_cfg["receivers"], msg)
        elif self.draft_cfg["type"] == "wechat":
            draft = WeChatDraft(title, self.draft_cfg["receivers"], msg)
        return draft

    def response(self) -> MessageDraft:
        with self.lock:
            if not self.report_condition.RESPONSE or self.state == ProcState.PROC_FINISH: return None
            res = self.actions.response_action()
            res = "\n".join(res)
            draft = self.create_draft(title=f"{self.name} - Response Report", msg=res)
            return draft
    
    def regular(self) -> MessageDraft:
        with self.lock:
            if not self.report_condition.REGULAR or self.state == ProcState.PROC_FINISH: return None
            res = self.actions.regular_action()
            res = "\n".join(res)
            draft = self.create_draft(title=f"{self.name} - Regular Report", msg=res)
            return draft
        
    def update(self, data: dict) -> MessageDraft:
        with self.lock:
            if self.state == ProcState.PROC_FINISH: return None
            self._datas.append(data)

            if not self.report_condition.UPDATE: return None
            res = self.actions.update_action()
            res = "\n".join(res)
            draft = self.create_draft(title=f"{self.name} - Update Report", msg=res)
            return draft
    
    def finish(self) -> MessageDraft:
        with self.lock:
            self.state = ProcState.PROC_FINISH

            if not self.report_condition.FINISH: return None
            res = self.actions.finish_action()
            res = "\n".join(res)
            draft = self.create_draft(title=f"{self.name} - Finish Report", msg=res)
            return draft
