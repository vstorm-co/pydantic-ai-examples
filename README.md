# PydanticAI Model Parameters Examples


### 1. Model Parameters
**Location**: `temperature/`

Control model behavior using temperature and other settings.

- Temperature effects on creativity vs consistency
- Practical configuration examples
- Use case recommendations

[View Example →](temperature/)

### 2. Reasoning Effort
**Location**: `reasoning_effort/`

Demonstrates reasoning_effort parameter for GPT-4o and o1 models.

- Control depth of internal reasoning
- Complex problem-solving examples
- Latency vs quality trade-offs

[View Example →](reasoning_effort/)

## Quick Start

### Setup
# Set API key
echo "OPENAI_API_KEY=your-key" > .env
```

### Run Examples

```bash

# Model parameters
cd temperature
uv run temperature_demo.py

# Reasoning effort 
cd reasoning_effort
uv run reasoning_demo.py

## Project Structure
```
├── temperature/
│   ├── temperature_demo.py
│   └── README.md
├── reasoning_effort/
│   ├── reasoning_demo.py
│   └── README.md
├── pyproject.toml
└── README.md
```