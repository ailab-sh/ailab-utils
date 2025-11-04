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
    # Create pages for similarity indexing
    page1 = client.create_page(
        page_id=1,
        text="Artificial intelligence is transforming how we work and live..."
    )

    page2 = client.create_page(
        page_id=2,
        text="Machine learning algorithms are revolutionizing data analysis..."
    )

    # Find similar pages
    similarities = client.find_similar(
        link_task_id=1,
        content="AI and machine learning are changing the world",
        page_ids=[1, 2],
        similarity_percentage=75.0
    )

    print(f"Found similarities: {similarities}")

    # Compare new questions against existing ones
    matches = client.compare_questions(
        new_questions=["What is AI?", "How does ML work?"],
        existing_questions=["Tell me about artificial intelligence", "Explain machine learning"],
        similarity_threshold=50.0
    )

    print(f"Question matches: {matches}")

except Exception as e:
    print(f"An error occurred: {e}")
```

### LLM Client
```python
from ailab_utils import LLMClient

client = LLMClient(api_key="your-api-key")

try:
    # List available models
    models = client.list_models()
    print(f"Available models: {[m['id'] for m in models]}")

    # Simple inference
    response = client.inference(
        model="deepseek-r1",
        prompt="What is 2+2?"
    )
    print(f"Response: {response['choices'][0]['message']['content']}")
    print(f"Tokens used: {response['usage']['total_tokens']}")

    # Inference with parameters
    response = client.inference(
        model="deepseek-r1",
        prompt="Explain quantum computing in one sentence.",
        temperature=0.7,
        max_tokens=100
    )
    print(f"Response: {response['choices'][0]['message']['content']}")

except Exception as e:
    print(f"An error occurred: {e}")
```

