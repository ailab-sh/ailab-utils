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

    def create_site(self, site_id: int, name: str, description: Optional[str] = None) -> dict:
        """Create a new site for organizing articles."""
        endpoint = f"{self.base_url}/api/sites"
        payload = {
            "idSite": site_id,
            "name": name
        }
        if description:
            payload["description"] = description
        
        response = requests.post(endpoint, headers=self.headers, json=payload, timeout=10)
        response.raise_for_status()
        return response.json()

    def get_sites(self) -> List[dict]:
        """Retrieve all sites."""
        endpoint = f"{self.base_url}/api/sites"
        response = requests.get(endpoint, headers=self.headers, timeout=10)
        response.raise_for_status()
        return response.json()

    def update_site(self, site_id: int, name: Optional[str] = None, description: Optional[str] = None) -> dict:
        """Update an existing site."""
        endpoint = f"{self.base_url}/api/sites/{site_id}"
        payload = {}
        if name is not None:
            payload["name"] = name
        if description is not None:
            payload["description"] = description
        
        response = requests.put(endpoint, headers=self.headers, json=payload, timeout=10)
        response.raise_for_status()
        return response.json()

    def delete_site(self, site_id: int) -> None:
        """Delete a site and all its articles."""
        endpoint = f"{self.base_url}/api/sites/{site_id}"
        response = requests.delete(endpoint, headers=self.headers, timeout=10)
        response.raise_for_status()

    def create_article(self, site_id: int, article_id: int, text: str) -> dict:
        """Create a new article in a site."""
        endpoint = f"{self.base_url}/api/articles"
        payload = {
            "idSite": site_id,
            "idArticleSnapshot": article_id,
            "text": text
        }
        
        response = requests.post(endpoint, headers=self.headers, json=payload, timeout=10)
        response.raise_for_status()
        return response.json()

    def get_articles(self, site_id: Optional[int] = None) -> List[dict]:
        """Retrieve articles, optionally filtered by site."""
        endpoint = f"{self.base_url}/api/articles"
        params = {}
        if site_id is not None:
            params["idSite"] = site_id
        
        response = requests.get(endpoint, headers=self.headers, params=params, timeout=10)
        response.raise_for_status()
        return response.json()

    def update_article(self, article_id: int, site_id: Optional[int] = None, text: Optional[str] = None) -> dict:
        """Update an existing article."""
        endpoint = f"{self.base_url}/api/articles/{article_id}"
        payload = {}
        if site_id is not None:
            payload["idSite"] = site_id
        if text is not None:
            payload["text"] = text
        
        response = requests.put(endpoint, headers=self.headers, json=payload, timeout=10)
        response.raise_for_status()
        return response.json()

    def delete_article(self, article_id: int) -> None:
        """Delete an article."""
        endpoint = f"{self.base_url}/api/articles/{article_id}"
        response = requests.delete(endpoint, headers=self.headers, timeout=10)
        response.raise_for_status()

    def find_similar(self, site_id: int, article_id: int, text: str) -> dict:
        """Find articles similar to the given text within a site."""
        endpoint = f"{self.base_url}/api/similarity"
        payload = {
            "idSite": site_id,
            "idArticleSnapshot": article_id,
            "text": text
        }
        
        response = requests.post(endpoint, headers=self.headers, json=payload, timeout=10)
        response.raise_for_status()
        return response.json()