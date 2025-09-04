import requests

class AITasksClient:
    def __init__(self, api_key: str, base_url: str = "https://ai-tasks.ailab.sh"):
        if not api_key:
            raise ValueError("API key cannot be empty.")
        
        self.api_key = api_key
        self.base_url = base_url.rstrip('/')
        self.headers = {
            "Content-Type": "application/json",
            "X-API-Key": self.api_key,
        }

    def submit_task(self, prompt: str, callback_url: str, provider: str = None) -> dict:
        endpoint = f"{self.base_url}/api/v1/tasks"
        payload = {
            "prompt": prompt,
            "callback_url": callback_url,
        }
        if provider:
            payload["provider"] = provider
        
        response = requests.post(endpoint, headers=self.headers, json=payload, timeout=10)
        
        response.raise_for_status()
        
        return response.json()