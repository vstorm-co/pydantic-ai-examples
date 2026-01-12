# PydanticAI Classification Examples


### 1. Basic Sentiment Classification
**Location**: `basic_sentiment/`

Fixed 3-class sentiment analysis (positive/negative/neutral) with structured outputs.

- Fixed Literal types defined at design time
- Simple accuracy evaluation
- Type-safe results with Pydantic validation

[View Example →](basic_sentiment/)

### 2. Dynamic Classification
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
# Basic sentiment classifier
cd basic_sentiment
uv run sentiment_classifier.py

# Dynamic classifier
cd dynamic_classification
uv run dynamic_classifier.py