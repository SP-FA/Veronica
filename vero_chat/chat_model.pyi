from typing import Type

class ChatModel:
    def __init__(self, path: str):
        self.params = None
    def chat(self): ...
    def update_data(self, role: str, content: str): ...

class Ernie(ChatModel):
    def __init__(self, path: str):
        self.url = None
        self.headers = None
        self.data = None
    def chat(self) -> str: ...
    def update_data(self, role: str, content: str): ...

class ChatGPT(ChatModel):
    def __init__(self, path):
        self.data = []
    def chat(self) -> str: ...
    def update_data(self, role: str, content: str): ...

class ChatSession:
    def __init__(self, name: str, model: Type, path: str):
        self.name = name
        self.model = None
    def gen_response(self, msg: str) -> str: ...
