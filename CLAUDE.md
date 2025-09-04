# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Python utility package that provides client libraries for AILab services. The main components are the `AITasksClient` for interacting with AILab's AI Tasks API and the `SimilarityClient` for document similarity search and retrieval.

## Project Structure

```
src/
└── ailab_utils/
    ├── __init__.py          # Main package entry point, exports AITasksClient and SimilarityClient
    ├── ai_tasks/
    │   ├── __init__.py      # AI Tasks module exports
    │   └── client.py        # AITasksClient implementation
    └── similarity/
        ├── __init__.py      # Similarity module exports
        └── client.py        # SimilarityClient implementation
```

The package follows a modular design where each service client is in its own submodule under `ailab_utils`. Currently implements AI Tasks and Similarity service clients.

## Development Commands

### Building and Installation
```bash
pip install -e .                    # Install in development mode
pip install build && python -m build # Build distribution packages
```

### Package Management
```bash
pip install git+https://github.com/ailab-sh/ailab-utils.git  # Install from GitHub
```

## Architecture

### AITasksClient
- **Location**: `src/ailab_utils/ai_tasks/client.py:3`
- **Purpose**: HTTP client for submitting tasks to AILab's AI Tasks API
- **Key Methods**:
  - `submit_task(prompt, callback_url, provider=None)` - Submit an AI task for processing
- **Configuration**: Accepts `api_key` (required) and `base_url` (defaults to `https://ai-tasks.ailab.sh`)
- **Dependencies**: Uses `requests` library for HTTP communication
- **Error Handling**: Validates API key on initialization, raises HTTP errors on failed requests

### SimilarityClient
- **Location**: `src/ailab_utils/similarity/client.py:4`
- **Purpose**: HTTP client for document similarity search and retrieval using AILab's Similarity API
- **Key Methods**:
  - **Site Management**:
    - `create_site(site_id, name, description=None)` - Create a new site for organizing articles
    - `get_sites()` - Retrieve all sites
    - `update_site(site_id, name=None, description=None)` - Update site information
    - `delete_site(site_id)` - Delete a site and all its articles
  - **Article Management**:
    - `create_article(site_id, article_id, text)` - Add a new article to a site for similarity indexing
    - `get_articles(site_id=None)` - Retrieve articles, optionally filtered by site
    - `update_article(article_id, site_id=None, text=None)` - Update article content or site assignment
    - `delete_article(article_id)` - Remove an article from the similarity index
  - **Similarity Search**:
    - `find_similar(site_id, article_id, text)` - Find articles similar to given text within a site
- **Configuration**: Accepts `api_key` (required) and `base_url` (defaults to `https://similarity.ailab.sh`)
- **Dependencies**: Uses `requests` library for HTTP communication
- **Error Handling**: Validates API key on initialization, raises HTTP errors on failed requests
- **Authentication**: Uses Bearer token authentication via Authorization header

### Package Configuration
- **Build System**: Uses setuptools with pyproject.toml configuration
- **Python Compatibility**: Requires Python >=3.8
- **Dependencies**: Only requires `requests>=2.20.0`
- **License**: MIT License

## Key Implementation Details

- The package uses a simple modular structure where each service gets its own submodule
- All client classes are exposed at the top level through `__init__.py` imports
- HTTP timeouts are set to 10 seconds for API calls
- **Authentication Patterns**:
  - AITasksClient: Uses `X-API-Key` header
  - SimilarityClient: Uses Bearer token in `Authorization` header
- Error handling follows standard HTTP status code patterns with `requests.raise_for_status()`
- **Similarity Service Architecture**:
  - Uses hierarchical organization: Sites contain Articles
  - Articles are indexed for similarity search using sentence embeddings
  - Similarity search is scoped within a site for better relevance
  - Supports CRUD operations for both sites and articles