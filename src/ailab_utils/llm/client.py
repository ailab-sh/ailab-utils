import json
import re
import time
from typing import List, Dict
import requests


class LLMClient:

    def __init__(self, api_key: str, base_url: str = "https://api.ailab.sh"):
        if not api_key:
            raise ValueError("API key cannot be empty.")

        self.api_key = api_key
        self.base_url = base_url.rstrip('/')
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}",
        }

    def list_models(self) -> List[Dict]:
        endpoint = f"{self.base_url}/v1/models"
        response = requests.get(endpoint, headers=self.headers, timeout=10)
        response.raise_for_status()
        return response.json().get("data", [])

    def inference(self, model: str, prompt: str, **kwargs) -> Dict:
        endpoint = f"{self.base_url}/v1/chat/completions"

        payload = {
            "model": model,
            "messages": [
                {"role": "user", "content": prompt}
            ]
        }

        payload.update(kwargs)
        payload["stream"] = True

        response = requests.post(
            endpoint,
            headers=self.headers,
            json=payload,
            stream=True,
            timeout=600
        )
        response.raise_for_status()

        full_content = ""
        response_id = None
        model_name = None
        created = None
        finish_reason = None

        for line in response.iter_lines(decode_unicode=True):
            if not line or not line.startswith("data: "):
                continue

            data = line[6:]
            if data == "[DONE]":
                break

            chunk = json.loads(data)

            if response_id is None:
                response_id = chunk.get("id")
                model_name = chunk.get("model")
                created = chunk.get("created")

            choices = chunk.get("choices", [])
            if choices:
                delta = choices[0].get("delta", {})
                content = delta.get("content", "")
                if content:
                    full_content += content

                if choices[0].get("finish_reason"):
                    finish_reason = choices[0]["finish_reason"]

        filtered_content = re.sub(r'<think>.*?</think>', '', full_content, flags=re.DOTALL)
        filtered_content = filtered_content.strip()

        result = {
            "id": response_id,
            "object": "chat.completion",
            "created": created if created is not None else int(time.time()),
            "model": model_name,
            "choices": [{
                "index": 0,
                "message": {
                    "role": "assistant",
                    "content": filtered_content
                },
                "finish_reason": finish_reason
            }],
            "usage": {
                "prompt_tokens": 0,
                "completion_tokens": 0,
                "total_tokens": 0
            }
        }

        return result
