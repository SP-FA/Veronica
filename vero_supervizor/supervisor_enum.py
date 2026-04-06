from typing import Dict
from enum import IntEnum, StrEnum


class ReportCondition:
    """表示进程报告条件的枚举

    Attributes:
        RESPONSE (boolean): 在询问时报告该进程状态
        FINISH (boolean): 在进程结束时报告该进程状态, default
        REGULAR (boolean): 每过一段时间报告该进程状态
        UPDATE (boolean): 进程状态更新时立即报告该进程状态
    """
    def __init__(self, condition:Dict):
        self.RESPONSE = condition.get("response", condition.get("RESPONSE", False))
        self.REGULAR = condition.get("regular", condition.get("REGULAR", False))
        self.UPDATE = condition.get("update", condition.get("UPDATE", False))
        self.FINISH = condition.get("finish", condition.get("FINISH", False))


class TaskType(StrEnum):
    REGISTER = "register"
    UPDATE = "update"
    FINISH = "finish"


class ProcState(IntEnum):
    """表示进程状态的枚举

    Attributes:
        PROC_PROCESSING: 进程正在运行
        PROC_FINISH: 进程终止
    """
    PROC_PROCESSING = 0
    PROC_FINISH = 1

