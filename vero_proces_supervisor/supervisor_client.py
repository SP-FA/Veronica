import socket
import json
from supervisor_enum import ProcReportCondition, ProcState, ProcRequestType

class ProcessSupervisorClient:
    def __init__(self, hostIP: str, port: int, reportCondition: list):
        self.reportCondition = reportCondition
        self.state = ProcState.PROC_PROCESSING
        self.isRegistered = False

        self.hostIP = hostIP
        self.hostPort = port
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def register(self):
        data = {
            "type": ProcRequestType.REGISTER,
            "msg": "Register a process.",
            "condition": self.reportCondition,
            "state": self.state
        }
        feedback = self._send_and_feedback(data)
        try:
            self.isRegistered = feedback["registered"]
        except:
            self.isRegistered = False

    def update(self, params):
        if self.isRegistered is False:
            self.register()
            return

        data = {
            "type": ProcRequestType.UPDATE,
            "msg": "Update process info.",
            "params": params,
            "state": self.state
        }
        self._send_and_feedback(data)

    def check(self):
        if self.isRegistered is False:
            self.register()

        if ProcReportCondition.RESPONSE not in self.reportCondition:
            return

        data = {
            "type": ProcRequestType.RESPONSE,
            "msg": "Required to response the process info.",
        }
        self._send_and_feedback(data)

    def _send_and_feedback(self, data: dict):
        self.client.connect((self.hostIP, self.hostPort))
        feedback = self.client.send(json.dumps(data).encode('utf-8'))
        print(f"Received parameters: {feedback}")
        self.client.close()
        return feedback
