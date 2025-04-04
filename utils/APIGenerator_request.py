from openai import OpenAI
import json
import requests
import os

class APIGenerator_request:
    def __init__(self,
        api_url : str = "http://123.129.219.111:3000/v1/chat/completions",
        api_key : str = "",
    ):
        self.api_url = api_url
        self.api_key = api_key
        # get api key from os environment
        if self.api_key == "":
            self.api_key = os.environ.get("API_KEY")
            
        if self.api_key is None:
            raise ValueError("Lack of API_KEY")
    
    def api_chat(self, system_info: str, messages: str, model: str, finish_try: int = 3):
        try:
            payload = json.dumps({
                "model": model,
                "messages": [
                    {"role": "system", "content": system_info},
                    {"role": "user", "content": messages}
                ]
            })

            headers = {
            'Authorization': f"Bearer {self.api_key}",
            'Content-Type': 'application/json',
            'User-Agent': 'Apifox/1.0.0 (https://apifox.com)'
            }
            # 请求 OpenAI API
            response = requests.post(self.api_url, headers=headers, data=payload, timeout=1800)
            print("response ", response)
            print("response.status_code", response.status_code)

            if response.status_code == 200:
                response_data = response.json()
                return response_data['choices'][0]['message']['content']


        except Exception as e:
            print("Error:", e)
            pass