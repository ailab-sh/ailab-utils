"""
LLM Inference Client for api.ailab.sh
"""
import json
import re
from typing import List, Dict, Optional
import requests


class LLMClient:
    """
    Client for interacting with the LLM Gateway API.

    Provides methods to list available models and perform inference.
    """

    def __init__(self, api_key: str, base_url: str = "https://api.ailab.sh"):
        """
        Initialize the LLM client.

        Args:
            api_key: API key for authentication
            base_url: Base URL of the LLM Gateway API

        Raises:
            ValueError: If api_key is empty
        """
        if not api_key:
            raise ValueError("API key cannot be empty.")

        self.api_key = api_key
        self.base_url = base_url.rstrip('/')
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}",
        }

    def list_models(self) -> List[Dict]:
        """
        Get list of available models.

        Returns:
            List of model dictionaries with id, object, created, and owned_by fields

        Raises:
            requests.HTTPError: If the request fails
        """
        endpoint = f"{self.base_url}/v1/models"
        response = requests.get(endpoint, headers=self.headers, timeout=10)
        response.raise_for_status()
        return response.json().get("data", [])

    def inference(
        self,
        model: str,
        prompt: str,
        **kwargs
    ) -> Dict:
        """
        Send inference request to the LLM.

        Uses streaming internally to avoid Cloudflare's 60-second timeout,
        then returns the complete response. Thinking content (<think> tags)
        is filtered out from the final response.

        Args:
            model: Model alias or name (e.g., "deepseek-r1", "GPT-OSS-120")
            prompt: User prompt/question
            **kwargs: Additional parameters (temperature, max_tokens, etc.)

        Returns:
            OpenAI-compatible response dictionary with:
            - id: Response ID
            - object: "chat.completion"
            - model: Model used
            - choices: List with message content and finish_reason

        Raises:
            requests.HTTPError: If the request fails
        """
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
            "model": model_name,
            "choices": [{
                "index": 0,
                "message": {
                    "role": "assistant",
                    "content": filtered_content
                },
                "finish_reason": finish_reason
            }]
        }

        if created is not None:
            result["created"] = created

        return result
