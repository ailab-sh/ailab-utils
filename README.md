# AILab Utilities Python Package

This package provides a collection of utility clients for interacting with AILab services.

## Installation
```bash
pip install git+https://github.com/ailab-sh/ailab-utils.git
```

## Usage

### AI Tasks Client
```python
from ailab_utils import AITasksClient

client = AITasksClient(api_key="secret-key-1")

try:
    result = client.submit_task(
        prompt="Why is the sky blue?",
        callback_url="http://my-server.com/callback"
    )
    print(f"Successfully submitted task: {result}")

except Exception as e:
    print(f"An error occurred: {e}")
```

### Similarity Client
```python
from ailab_utils import SimilarityClient

client = SimilarityClient(api_key="secret-key-1")

try:
    # Create a site for organizing articles
    site = client.create_site(
        site_id=1,
        name="Tech Blog",
        description="Articles about technology"
    )
    
    # Add an article to the site
    article = client.create_article(
        site_id=1,
        article_id=1001,
        text="Artificial intelligence is transforming how we work and live..."
    )
    
    # Find similar articles
    similarities = client.find_similar(
        site_id=1,
        article_id=1001,
        text="AI and machine learning are changing the world"
    )
    
    print(f"Found {len(similarities['similarities'])} similar articles")

except Exception as e:
    print(f"An error occurred: {e}")
```

