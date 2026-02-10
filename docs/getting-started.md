---
title: Getting Started
---

# Getting Started

## Prerequisites

- **Python 3.10+**
- **[uv](https://docs.astral.sh/uv/)** package manager

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/vstorm-co/pydantic-ai-examples.git
cd pydantic-ai-examples
```

### 2. Install dependencies

```bash
uv sync
```

### 3. Configure your API key

```bash
echo "OPENAI_API_KEY=your-key-here" > .env
```

!!! warning "API Key Required"
    Most examples use OpenAI's GPT-5.1. Ensure your API key has appropriate permissions and sufficient quota.

!!! tip "Bielik Example"
    The Bielik example uses a local model via Ollama and does **not** require an OpenAI key. See the [Bielik setup](examples/bielik.md#prerequisites) for details.

## Running Examples

Each example lives in its own directory and can be run independently:

```bash
# Pick any example directory
cd direct_model_request
uv run direct_request_demo.py
```

See the [Examples Overview](examples/index.md) for the full list and recommended learning path.

## Troubleshooting

### API Key Issues

- Ensure `OPENAI_API_KEY` is set in your `.env` file
- Verify your key has appropriate permissions
- Check for rate limiting (503 errors)

### Import Errors

- Run `uv sync` to install all dependencies
- Verify you're using Python 3.10+

### Async Issues

- Some examples require async-compatible event loops
- On Windows, you may need to set the event loop policy

### OCR-Specific Issues

- **poppler not found**: Install via your package manager (`brew install poppler` / `apt install poppler-utils` / `choco install poppler`)
- **PDF conversion fails**: Ensure the PDF is valid and readable
- **Rate limiting**: Reduce the semaphore value in `ocr_parsing/shared_fns.py`

See individual example pages for specific setup requirements.
