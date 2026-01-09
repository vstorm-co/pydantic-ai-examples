# PydanticAI Examples


### 1. Direct Model Requests
**Location**: `direct_model_request/`

Demonstrates direct model API calls without using Agents.

- Basic synchronous model requests using gpt-5.2
- When to use direct API vs Agents
- Simple text prompt handling

[View Example →](direct_model_request/)

### 2. Model Parameters
**Location**: `temperature/`

Control model behavior using temperature.

- Temperature effects on creativity vs consistency
- Practical configuration examples
- Use case recommendations

[View Example →](temperature/)

### 3. Reasoning Effort
**Location**: `reasoning_effort/`

Demonstrates reasoning_effort parameter for gpt-5.2.

- Control depth of internal reasoning
- Complex problem-solving examples

[View Example →](reasoning_effort/)

## Quick Start

### Setup

```bash
# Install dependencies
uv sync

# Set API key
echo "OPENAI_API_KEY=your-key" > .env
```

### Run Examples
```bash
# Direct model requests
cd direct_model_request
uv run direct_request_demo.py

# Model parameters
cd temperature
uv run temperature_demo.py

# Reasoning effort 
cd reasoning_effort
uv run reasoning_demo.py
```

## Project Structure
```bash
├── direct_model_request/
│   ├── direct_request_demo.py
│   └── README.md
├── temperature/
│   ├── temperature_demo.py
│   └── README.md
├── reasoning_effort/
│   ├── reasoning_demo.py
│   └── README.md
├── pyproject.toml
└── README.md
```