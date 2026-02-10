---
title: Basic Sentiment
---

# Basic Sentiment Classification

Simple sentiment analysis using PydanticAI with fixed classification classes.

## Overview

This example demonstrates:

- Fixed `Literal` types for classification (`positive`, `negative`, `neutral`)
- Structured output with Pydantic models
- Field validation and descriptions
- Basic accuracy evaluation

## Structure

```python
class SentimentResult(BaseModel):
    sentiment: Literal["positive", "negative", "neutral"]
    reasoning: str
```

The agent is constrained to return exactly one of the three predefined sentiment classes.

## Running

```bash
cd basic_sentiment
uv run sentiment_classifier.py
```

## Output

```
Sentiment Analysis with PydanticAI
======================================================================

Review 1/10:
Text: This product is absolutely amazing! Best purchase ever!

Classification:
  Sentiment: positive
  Reasoning: Strong enthusiastic language indicates positive sentiment
  Expected: positive
  Status: Correct
```

## Key Concepts

!!! info "Fixed Classes"
    Classes are defined at design time in the `Literal` type. Pydantic ensures only valid sentiments are returned — the model **cannot** produce a value outside the allowed set.

- **Type Safety** — Results are validated Pydantic models
- **Structured Output** — The agent returns a `SentimentResult`, not raw text
- **Evaluation** — Compare predictions against expected labels for accuracy measurement

!!! tip "Next Step"
    Want categories that change at runtime? See [Dynamic Classification](dynamic-classification.md).
