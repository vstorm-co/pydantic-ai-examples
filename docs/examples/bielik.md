---
title: Bielik (Local Models)
---

# Bielik Examples with PydanticAI

An educational guide to using **Bielik**, a Polish language LLM model, with the PydanticAI framework. These examples show how to build AI agents with local language models served via Ollama.

## What is Bielik?

[Bielik](https://bielik.ai/) is a Polish language LLM, fine-tuned specifically for Polish language understanding and generation. It excels at:

- Polish language comprehension and generation
- Following instructions in Polish
- Maintaining context in conversations
- Tool calling (in supported versions)

You can find the model on [Hugging Face](https://huggingface.co/speakleash/Bielik-11B-v3.0-Instruct) and learn more on the [official Bielik website](https://bielik.ai/).

Running Bielik locally via Ollama gives you a private, cost-free alternative to cloud-based LLMs, with full control over your data.

## Prerequisites

### 1. Install Ollama

Download and install from [ollama.com](https://ollama.com). Mac users can use Homebrew:

```bash
brew install ollama
```

### 2. Pull the Bielik Model

```bash
ollama pull SpeakLeash/bielik-11b-v3.0-instruct:Q8_0
```

!!! tip "Try Different Models"
    You can try different versions of the model — just remember to update the name in the `Modelfile` as well. Browse available models at [ollama.com/search](https://ollama.com/search).

### 3. Create a custom version with the provided Modelfile

```bash
ollama create bielik_v3_q8_tools -f Modelfile
```

### 4. Serve and run the model

```bash
# Start the Ollama server
ollama serve

# In another terminal — make model available
ollama run bielik_v3_q8_tools

# Leave the prompt input by writing /bye

# Verify the model is being served
ollama ps
```

This starts an OpenAI-compatible API server on `http://localhost:11434/v1`.

### 5. Install dependencies

From the project root:

```bash
uv sync
```

### 6. (Optional) Set up Weather API

For the tools example, get a free API key from [weatherapi.com](https://www.weatherapi.com/) and create a `.env` file in the `bielik_example/` directory:

```bash
WEATHER_API_KEY=your_key_here
```

## Examples

### Example 1: Basic Inference

**File:** `bielik_basic_inference.py`

The simplest example — setting up a connection to the local Bielik model, creating a PydanticAI Agent, making a synchronous inference request, and retrieving token usage statistics.

```python
from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIChatModel
from pydantic_ai.providers.ollama import OllamaProvider

# Connect to the Bielik model served locally via Ollama
ollama_model = OpenAIChatModel(
    model_name="bielik_v3_q8_tools",
    provider=OllamaProvider(base_url="http://localhost:11434/v1"),
)

# Create an agent with a Polish system prompt
agent = Agent(ollama_model, system_prompt="Jesteś asystentem AI odpowiadającym krótko i zwięźle")


async def main():
    result = await agent.run("Cześć, kim jesteś?")  # "Hello, who are you?"
    print(f"Response: {result.output}")
    print(f"Token usage: {result.usage()}")
```

```bash
cd bielik_example
uv run python bielik_example/bielik_basic_inference.py
```

### Example 2: Tool Calling

**File:** `bielik_basic_tools.py`

Demonstrates custom tools with `@agent.tool`, multi-turn conversations with message history, async operations, and handling tool results.

**Tools included:**

1. **roll_dice** — Simulates rolling a 6-sided dice (no external dependencies)
2. **check_weather** — Fetches real weather data via API (requires weather API key)

```python
import secrets
from typing import Any

import httpx
from pydantic_ai import Agent, RunContext
from pydantic_ai.models.openai import OpenAIChatModel
from pydantic_ai.providers.ollama import OllamaProvider

ollama_model = OpenAIChatModel(
    model_name="bielik_v3_q8_tools",
    provider=OllamaProvider(base_url="http://localhost:11434/v1"),
)

agent = Agent(ollama_model, system_prompt="Jesteś pomocnym asystentem AI")


@agent.tool
async def roll_dice(ctx: RunContext[None]) -> int:
    """Simulates rolling a standard 6-sided dice."""
    return secrets.choice([1, 2, 3, 4, 5, 6])


@agent.tool
async def check_weather(ctx: RunContext[None], city: str) -> Any:
    """Fetches real-time weather data for a specified city."""
    url = "https://api.weatherapi.com/v1/current.json"
    params = {"key": WEATHER_API_KEY, "q": city, "aqi": "no"}

    async with httpx.AsyncClient() as client:
        response = await client.get(url, params=params)
        if response.status_code == 200:
            data = response.json()
            return {
                "location": data["location"]["name"],
                "temp_c": data["current"]["temp_c"],
                "condition": data["current"]["condition"]["text"],
            }
        return f"Error: Could not find weather for {city}"


async def main():
    # Multi-turn conversation with message history
    result_1 = await agent.run("Cześć, kim jesteś?")
    result_2 = await agent.run("Rzuć kostką!", message_history=result_1.all_messages())
    result_3 = await agent.run(
        "Sprawdź pogodę w Warszawie!", message_history=result_2.all_messages()
    )
    print(f"Response: {result_3.output}")
```

```bash
cd bielik_example
uv run python bielik_example/bielik_basic_tools.py
```

## Key Concepts

### Agent

An `Agent` wraps the language model, manages conversation history, coordinates tool calling, and processes user requests.

### Tools

Tools are functions decorated with `@agent.tool` that extend an agent's capabilities. They can be synchronous or asynchronous, receive a `RunContext` parameter, and make external API calls.

### Message History

PydanticAI maintains full conversation history for multi-turn interactions, context preservation, and tool call tracking via `result.all_messages()`.

## Troubleshooting

!!! warning "Connection refused"
    Make sure Ollama is running (`ollama serve` in a separate terminal) and listening on `http://localhost:11434`.

!!! warning "Model not found"
    Pull the model first: `ollama pull SpeakLeash/bielik-11b-v3.0-instruct:Q8_0`

!!! warning "Model running slowly"
    Bielik-11b is an 11 billion parameter model. Performance depends on your hardware — GPU is significantly faster than CPU. Consider smaller quantizations (Q4, Q5) if needed.

## Further Resources

- [PydanticAI Documentation](https://ai.pydantic.dev/)
- [Ollama Documentation](https://github.com/ollama/ollama)
- [Bielik Website](https://bielik.ai/)
- [Bielik on Hugging Face](https://huggingface.co/speakleash/Bielik-11B-v3.0-Instruct)
- [WeatherAPI Documentation](https://www.weatherapi.com/docs/)
