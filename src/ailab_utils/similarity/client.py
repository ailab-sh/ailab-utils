import requests
from typing import List, Dict, Any, Optional

class SimilarityClient:
    def __init__(self, api_key: str, base_url: str = "https://similarity.ailab.sh"):
        if not api_key:
            raise ValueError("API key cannot be empty.")

        self.api_key = api_key
        self.base_url = base_url.rstrip('/')
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}",
        }

    def create_page(self, page_id: int, text: str) -> dict:
        """Create a new page for similarity indexing."""
        endpoint = f"{self.base_url}/api/pages"
        payload = {
            "idPage": page_id,
            "text": text
        }

        response = requests.post(endpoint, headers=self.headers, json=payload, timeout=10)
        response.raise_for_status()
        return response.json()

    def get_pages(self) -> List[dict]:
        """Retrieve all pages."""
        endpoint = f"{self.base_url}/api/pages"
        response = requests.get(endpoint, headers=self.headers, timeout=10)
        response.raise_for_status()
        return response.json()

    def get_page(self, page_id: int) -> dict:
        """Retrieve a specific page by ID."""
        endpoint = f"{self.base_url}/api/pages/{page_id}"
        response = requests.get(endpoint, headers=self.headers, timeout=10)
        response.raise_for_status()
        return response.json()

    def update_page(self, page_id: int, text: str) -> dict:
        """Update an existing page."""
        endpoint = f"{self.base_url}/api/pages/{page_id}"
        payload = {
            "text": text
        }

        response = requests.put(endpoint, headers=self.headers, json=payload, timeout=10)
        response.raise_for_status()
        return response.json()

    def delete_page(self, page_id: int) -> None:
        """Delete a page."""
        endpoint = f"{self.base_url}/api/pages/{page_id}"
        response = requests.delete(endpoint, headers=self.headers, timeout=10)
        response.raise_for_status()

    def find_similar(self, link_task_id: int, content: str, page_ids: List[int], similarity_percentage: float = 75.0) -> dict:
        """Find pages similar to the given content within the specified pages."""
        endpoint = f"{self.base_url}/api/similarity"
        payload = {
            "idLinkTask": link_task_id,
            "content": content,
            "pages": page_ids,
            "similarityPercentage": similarity_percentage
        }

        response = requests.post(endpoint, headers=self.headers, json=payload, timeout=10)
        response.raise_for_status()
        return response.json()