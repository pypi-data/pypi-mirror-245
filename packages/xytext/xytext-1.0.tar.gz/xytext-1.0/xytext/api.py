import requests
import json

class XytextResponse:
    def __init__(self, response):
        self.raw_response = response
        self.success = response.get('success', False)
        self.usage = type('Usage', (), response.get('usage', {}))
        self.call_id = response.get('call_id', None)

        # Handle the 'result' attribute
        result_str = response.get('result')
        if result_str:
            try:
                self.result = json.loads(result_str)
            except json.JSONDecodeError:
                self.result = result_str
        else:
            self.result = None

class Xytext:
    def __init__(self, func_id, stage, auth_token):
        self.base_url = "https://api.xytext.com/invoke"
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {auth_token}"
        }
        self.func_id = func_id
        self.stage = stage

    def invoke(self, input_text):
        payload = {
            "input": input_text,
            "func_id": self.func_id,
            "stage": self.stage
        }
        response = requests.post(self.base_url, json=payload, headers=self.headers)
        return XytextResponse(response.json())
