"""
LLM Inference Client for api.ailab.sh
"""
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

        Args:
            model: Model alias or name (e.g., "deepseek-r1", "GPT-OSS-120")
            prompt: User prompt/question
            **kwargs: Additional parameters (temperature, max_tokens, stream, etc.)

        Returns:
            OpenAI-compatible response dictionary with:
            - id: Response ID
            - object: "chat.completion"
            - created: Unix timestamp
            - model: Model used
            - choices: List with message content and finish_reason
            - usage: Token usage (prompt_tokens, completion_tokens, total_tokens)

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

        # Add any additional parameters from kwargs
        payload.update(kwargs)

        response = requests.post(
            endpoint,
            headers=self.headers,
            json=payload,
            timeout=60
        )
        response.raise_for_status()
        return response.json()
