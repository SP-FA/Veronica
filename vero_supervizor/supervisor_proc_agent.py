from vero_supervizor.supervisor_enum import ProcState


class ProcessAgentActions:
    """表示一个被监控的进程的可用操作
    """
    def __init__(self, custom_actions: dict):
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
        for action in self.custom_actions.get(task, []):
            print(f"Executing {task} action: {action['name']} - {action['description']}")
            action["func"](self.agent)

    def init_action(self, agent):
        """在进程注册时执行的操作
        """
        self.agent = agent
        self.run_custom_action("init")
    
    def response_action(self):
        """在询问时执行的操作
        """
        self.run_custom_action("response")

    def regular_action(self):
        """定期执行的操作
        """
        self.run_custom_action("regular")

    def update_action(self):
        """在进程状态更新时执行的操作
        """
        self.run_custom_action("update")

    def finish_action(self):
        """在进程完成时执行的操作
        """
        self.run_custom_action("finish")


class ProcessAgent:
    """表示一个被监控的进程
    """
    def __init__(self, name: str, report_condition: dict, actions: ProcessAgentActions):
        self.name = name
        self.report_condition = report_condition
        self.actions = actions
        self.state = ProcState.PROC_PROCESSING
        self._datas = []  # 存储该进程的监控数据

        self.actions.init_action(self)
    
    def response(self):
        if not self.report_condition.RESPONESE: return
        self.actions.response_action()
    
    def regular(self):
        if not self.report_condition.REGULAR: return
        self.actions.regular_action()
    
    def update(self, data: dict):
        self._datas.append(data)

        if not self.report_condition.UPDATE: return
        self.actions.update_action()
    
    def finish(self):
        self.state = ProcState.PROC_FINISH

        if not self.report_condition.FINISH: return
        self.actions.finish_action()
