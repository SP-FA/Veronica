import requests
import json
from openai import OpenAI

from utils.configure_util import ConfLoader

class ChatModel:
    def __init__(self, path):
        self.params = ConfLoader(path)

    def chat(self):
        raise NotImplementedError

    def update_data(self, role, content):
        raise NotImplementedError


class Ernie(ChatModel):  # ERNIE-Bot 4.0
    def __init__(self, path):
        super().__init__(path)
        access_token = self.params["ernie_access_token"]
        self.url = f"https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/completions_pro?access_token={access_token}"
        self.headers = {
            'Content-Type': 'application/json',
        }
        self.data = {
            'messages': [
                {
                    'role': 'user',
                    'content': '你是谁？'
                },
                {
                    'role': 'assistant',
                    'content': '我是 Veronica'
                }
            ]
        }

    def chat(self):
        jsonData = json.dumps(self.data)
        response = requests.request("POST", self.url, headers=self.headers, data=jsonData)
        result = response.json().get("result")
        return result

    def update_data(self, role, content):
        self.data["messages"].append({
            'role': role,
            'content': content
        })


class ChatGPT(ChatModel):
    def __init__(self, path):
        """
        TODO: 在 params 里面添加是否是中转 key，是的话判断 openai 版本，选择不同的方式。
        """
        super().__init__(path)
        # openai.api_key = self.params["openai_key"]
        # if "openai_base" in self.params.params.keys():
        #     openai.api_base = self.params["openai_base"]
        # self.client = OpenAI(
        #     base_url=
        #     api_key=
        # )
        self.client = OpenAI(
            api_key=self.params["openai_key"],
            base_url=self.params["openai_base"]
        )
        self.data = []

    def chat(self):
        # response = openai.ChatCompletion.create(
        #     model="gpt-3.5-turbo",
        #     messages=self.data
        # )
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=self.data
        )
        # result = response["choices"][0]["message"]["content"]
        result = response.choices[0].message.content
        return result

    def update_data(self, role, content):
        self.data.append({
            'role': role,
            'content': content
        })


class ChatSession:
    """实现一个新的会话

    Attribute:
        name (str): 会话的标题
        model (Type): 一个 class 名字，Ernie 或者 ChatGPT
    """
    def __init__(self, name, model=ChatGPT, path="../conf.yaml"):
        self.name = name
        # if model.lower() == "ernie": self.model = Ernie(path)
        # if model.lower() == "chatgpt": self.model = ChatGPT(path)
        self.model = model(path)

    def gen_response(self, msg):
        self.model.update_data("user", msg)
        res = self.model.chat()
        self.model.update_data('assistant', res)
        return res


if __name__ == '__main__':
    chat = ChatSession('yzc', ChatGPT, path="../conf.yaml")
    for i in range(3):
        ques = input(f"[{i}] You:\n\t")
        res = chat.gen_response(ques)
        print(f"[{i}] Veronica:\n\t{res}")
