# Bielik Examples with PydanticAI

An educational guide to using **Bielik**, a Polish language LLM model, with the **PydanticAI** framework. This directory contains progressively advanced examples showing how to build AI agents with local language models.

## What is Bielik?

Bielik is a Polish language LLM, fine-tuned specifically for Polish language understanding and generation. It excels at:

- Polish language comprehension and generation
- Following instructions in Polish
- Maintaining context in conversations
- Tool calling (in supported versions)

Running Bielik locally via Ollama gives you a private, cost-free alternative to cloud-based LLMs, with full control over your data.

## Prerequisites

### 1. Install Ollama

- Download and install from [ollama.com](https://ollama.com)
- Ollama provides an easy way to run large language models locally

**Mac users** can download ollama via `homebrew` package manager:

```bash
brew install ollama
```

### 2. Pull the Bielik Model

Open a terminal and run:

```bash
# For tool calling (larger model, supports function calls)
ollama pull SpeakLeash/bielik-11b-v3.0-instruct:Q8_0
```

> **HINT**: You can try different versions of the model. However remember to change it's name also in the `Modelfile`.
If you'd like to try out even different models, head to [this address](https://ollama.com/search).

### 3. Create a custom version with provided Modelfile

```bash
ollama create bielik_v3_q8_tools -f Modelfile
```

### 4. Serve the Model

In current terminal, start the Ollama server:

```bash
ollama serve
```

This starts an OpenAI-compatible API server on `http://localhost:11434/v1`

### 5. Run the model in inference server

```bash
# Make model available at address above
ollama run bielik_v3_q8_tools

# Leave the prompt input by writing `/bye`

# Inspect if the model is being served
ollama ps
```

### 6. Install Dependencies

From this project's root directory:

```bash
pip install -r requirements.txt
# or if using uv:
uv sync
```

### 7. (Optional) Set Up Weather API

For the tools example, you'll need a free API key:

1. Visit [weatherapi.com](https://www.weatherapi.com/)
2. Sign up for a free account
3. Create a `.env` file in this directory:

   ```
   WEATHER_API_KEY=your_key_here
   ```

## Running the Examples

### Example 1: Basic Inference

**File**: `bielik_basic_inference.py`

This is the simplest example showing:

- Setting up a connection to the local Bielik model
- Creating a PydanticAI Agent
- Making a synchronous inference request
- Retrieving the response and token usage statistics

**Run**:

```bash
# with uv:
uv run python bielik_example/bielik_basic_inference.py
```

### Example 2: Tool Calling

**File**: `bielik_basic_tools.py`

This advanced example demonstrates:

- Defining custom tools using the `@agent.tool` decorator
- Tool calling: the model requests to use a tool when needed
- Multi-turn conversations with message history
- Asynchronous operations (like API calls)
- Handling tool results and incorporating them into responses

**Tools included**:

1. **roll_dice**: Simulates rolling a 6-sided dice (no external dependencies)
2. **check_weather**: Fetches real weather data via API (requires weather API key)

**Run**:

```bash
# with uv:
uv run python bielik_example/bielik_basic_tools.py
```


## Key Concepts Explained

### Agent

A `Agent` is the main interface for interacting with an LLM. It:

- Wraps the language model
- Manages conversation history
- Coordinates tool calling
- Processes user requests and returns responses

### Tools

Tools are functions that extend an agent's capabilities. They:

- Are decorated with `@agent.tool`
- Can be synchronous or asynchronous
- Receive a `RunContext` parameter
- Can make external API calls, perform calculations, etc.
- Are automatically available to the model for tool calling

### Message History

PydanticAI maintains full conversation history, allowing:

- Multi-turn interactions
- Context preservation across requests
- Tool call history and results
- Access via `result.all_messages()`

### RunContext

Provides access to:

- Agent state during tool execution
- Message history
- Any custom context passed to the agent

## Troubleshooting

### "Connection refused" error

**Issue**: Can't connect to Ollama
**Solution**:

1. Make sure Ollama is running: `ollama serve` in a separate terminal
2. Check that it's listening on `http://localhost:11434`

### Model not found error

**Issue**: Model `bielik` or `bielik_v3_q8_tools` not found
**Solution**:

```bash
# or for tools support:
ollama pull SpeakLeash/bielik-11b-v3.0-instruct:Q8_0
```

### Weather API returns 401 error

**Issue**: API key is invalid or not set
**Solution**:

1. Double-check your API key from weatherapi.com
2. Ensure `.env` file has `WEATHER_API_KEY=your_actual_key`
3. Restart the script after changing `.env`

### Model running slowly

**Issue**: Inference takes a long time
**Solution**:

- Bielik-11b is a 11 billion parameter model; slower hardware will be slower
- The Q8_0 quantization reduces memory but not much speed
- Consider using smaller quantizations (Q4, Q5) if available
- Model performance depends on your hardware (GPU faster than CPU)

## File Structure

```
bielik_example/
├── README.md                          # This file
├── bielik_basic_inference.py          # Example 1: Simple inference
├── bielik_basic_tools.py              # Example 2: Tool calling
├── Modelfile                           # Ollama model configuration
└── (optional) .env                    # Environment variables for API keys
```

## What's in the Modelfile?

The `Modelfile` configures how Bielik handles tool calling:

- Defines the prompt template for tool calling
- Sets up special tokens for tool calls
- Configures temperature (0.1 for deterministic outputs)
- Specifies context window (8192 tokens)


## Further Resources

- [PydanticAI Documentation](https://ai.pydantic.dev/)
- [Ollama Documentation](https://github.com/ollama/ollama)
- [Bielik Model Repository](https://huggingface.co/SpeakLeash/bielik-11b-v3.0-instruct)
- [WeatherAPI Documentation](https://www.weatherapi.com/docs/) (for tools example)
