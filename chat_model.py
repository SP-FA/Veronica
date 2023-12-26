import requests
import json
import openai


class ChatModel:
    def chat(self):
        raise NotImplementedError

    def update_data(self, role, content):
        raise NotImplementedError


access_token = "24.16af52018cd524ca8fa5d3133dfd6c09.2592000.1705601666.282335-45332416"


class Ernie(ChatModel):  # ERNIE-Bot 4.0
    def __init__(self):
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
                    'content': '我是 Veronica，一位赛博管家。'
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
    def __init__(self):
        openai.api_key = "sk-oqJn98z22yZNRRoa2cDe012cF65849048f84D3BaBe6e1c69"
        openai.api_base = "https://oneapi.xty.app/v1"
        # self.client = OpenAI(
        #     base_url="https://oneapi.xty.app/v1",
        #     api_key="sk-oqJn98z22yZNRRoa2cDe012cF65849048f84D3BaBe6e1c69"
        # )
        self.data = []

    def chat(self):
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=self.data
        )
        result = response["choices"][0]["message"]["content"]
        return result

    def update_data(self, role, content):
        self.data.append({
            'role': role,
            'content': content
        })


class ChatData:
    def __init__(self, name, model="chatgpt"):
        self.name = name
        if model.lower() == "ernie": self.model = Ernie()
        if model.lower() == "chatgpt": self.model = ChatGPT()

    def gen_response(self, msg):
        self.model.update_data("user", msg)
        res = self.model.chat()
        self.model.update_data('assistant', res)
        return res


if __name__ == '__main__':
    chat = ChatData('yzc', "chatgpt")
    for i in range(3):
        ques = input(f"[{i}] You:\n\t")
        res = chat.gen_response(ques)
        print(f"[{i}] Veronica:\n\t{res}")

