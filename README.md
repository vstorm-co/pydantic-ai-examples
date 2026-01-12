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

### 4. Basic Sentiment Classification

**Location**: `basic_sentiment/`

Fixed 3-class sentiment analysis (positive/negative/neutral) with structured outputs.

- Fixed Literal types defined at design time
- Simple accuracy evaluation
- Type-safe results with Pydantic validation

[View Example →](basic_sentiment/)

### 5. Dynamic Classification

**Location**: `dynamic_classification/`

Runtime-adaptable classification that handles any number of classes dynamically.

- Dynamic Literal type generation using `create_model()`
- Same code handles binary, multi-class, and fine-grained classification

[View Example →](dynamic_classification/)

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

# Basic sentiment classifier
cd basic_sentiment
uv run sentiment_classifier.py

# Dynamic classifier
cd dynamic_classification
uv run dynamic_classifier.py
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
├── basic_sentiment/
│   ├── sentiment_classifier.py
│   └── README.md
├── dynamic_classification/
│   ├── dynamic_classifier.py
│   └── README.md
├── pyproject.toml
└── README.md
```
