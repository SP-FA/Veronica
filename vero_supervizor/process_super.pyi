import psutil
from typing import List, Dict


class Timer:
    TIMER_OFF = 0
    TIMER_ON = 1

class ProcState:
    PROC_RESPONSE = 0
    PROC_FINISH = 1
    PROC_REGULAR = 2

class Supervisor:
    def __init__(self):
        self.user = None
        self.allProcess = []

    def find_process(self) -> List[Dict]: ...
    def find_registered_process(self, procList: List[psutil.Process] = None) -> List[psutil.Process]: ...
    def get_finished_process(self) -> List[psutil.Process]: ...

