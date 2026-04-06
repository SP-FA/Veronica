import socket
import json
import threading
import queue
import time

from utils import VERO_SUPERVISOR_LOG_DIR, get_logger
from vero_supervizor import TaskType


logger = get_logger(__name__, VERO_SUPERVISOR_LOG_DIR, log_filename="supervisor_client.log")


class SupervisorDataFactory:
    _factory_obj = None

    def __new__(cls, *args, **kwargs):
        if cls._factory_obj is None:
            obj = super().__new__(cls)
            obj.proc_lst = []
            cls._factory_obj = obj
        return cls._factory_obj

    def register(
        self, 
        proc_name, 
        data, 
        response: bool=False, 
        regular: bool=False, 
        update: bool=False, 
        finish: bool=False
    ):
        if proc_name in self.proc_lst:
            logger.warning(f"{proc_name} has already been used")
        else:
            self.proc_lst.append(proc_name)

        condition = {
            "response": response,
            "regular": regular,
            "update": update,
            "finish": finish,
        }
        return {
            "task": TaskType.REGISTER.value,
            "proc_name": proc_name,
            "report_condition": condition,
            "data": data,
        }
    
    def update(self, proc_name, data):
        if proc_name not in self.proc_lst:
            logger.warning(f"{proc_name} has not been registered yet")
            return self.register(proc_name, data)

        return {
            "task": TaskType.UPDATE.value,
            "proc_name": proc_name,
            "data": data,
        }

    def finish(self, proc_name):
        if proc_name not in self.proc_lst:
            logger.warning(f"{proc_name} has not been registered yet")
            return None
        
        return {
            "task": TaskType.FINISH.value,
            "proc_name": proc_name,
        }


class SupervisorClient:
    def __init__(self, host='127.0.0.1', port=5000, max_queue_size=1000):
        self.host = host
        self.port = port
        self.queue = queue.Queue(maxsize=max_queue_size)
        self.sock = None
        self.running = True

        t = threading.Thread(target=self._worker, daemon=True)
        t.start()

    def _connect(self):
        while self.running:
            try:
                self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.sock.connect((self.host, self.port))
                logger.info("Supervisor client connected")
                return
            except Exception as e:
                logger.error("Supervisor client connect failed: %s", e)
                logger.error("Retrying...")
                time.sleep(2)

    def _worker(self):
        self._connect()

        while self.running:
            try:
                data = self.queue.get(timeout=1)

                msg = json.dumps(data).encode('utf-8')
                length = len(msg).to_bytes(4, 'big')  # 解决粘包

                self.sock.sendall(length + msg)

            except queue.Empty:
                continue
            except Exception as e:
                logger.error("Supervisor client send error: %s", e)
                self._connect()

    def send(self, data):
        try:
            self.queue.put_nowait(data)
        except queue.Full:
            logger.warning("Queue full, dropping data")

    def close(self):
        self.running = False
        if self.sock:
            self.sock.close()
