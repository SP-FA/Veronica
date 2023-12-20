import requests
import json

access_token = "24.16af52018cd524ca8fa5d3133dfd6c09.2592000.1705601666.282335-45332416"


class Ernie:  # ERNIE-Bot 4.0
    def __init__(self):
        self.url = f"https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/completions_pro?access_token={access_token}"
        self.headers = {
            'Content-Type': 'application/json',
        }

    def chat(self, data):
        jsonData = json.dumps(data)
        response = requests.request("POST", self.url, headers=self.headers, data=jsonData)
        result = response.json().get("result")
        return result


if __name__ == '__main__':
    chat = ChatModel()
    for i in range(3):
        ques = input(f"[{i}] You:\n\t")
        chat.add_data('user', ques)
        res, data = chat.chat()
        print(f"[{i}] Veronica:\n\t{res}")
