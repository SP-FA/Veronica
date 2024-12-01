class ProcReportCondition:
    """表示进程报告条件的枚举

    Attributes:
        RESPONSE: 在询问时报告该进程状态
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


class ProcRequestType:
    """表示进程请求类型

    Attributes:
        REGISTER: 注册一个新进程
        UPDATE: 更新进程状态
        RESPONSE: 要求报告进程状态
    """
    REGISTER = 0
    UPDATE = 1
    RESPONSE = 2
