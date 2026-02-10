---
title: Dynamic Classification
---

# Dynamic Classification

Runtime-adaptable classification using dynamically generated Literal types.

## Overview

This example demonstrates how to build a classifier that adapts to **any number of classes** at runtime, using Pydantic's `create_model()` to generate dynamic Literal types.

## Key Technique

The core idea is to create a Pydantic model with a dynamic `Literal` type at runtime, then pass it as `output_type` to a PydanticAI `Agent`:

```python
from typing import Any, Literal

from pydantic import BaseModel, Field, create_model
from pydantic_ai import Agent


def create_dynamic_classifier_model(classes: list[str]) -> type[BaseModel]:
    """Dynamically create a Pydantic model with runtime-defined Literal classes."""
    literal_type = Literal[*tuple(classes)]  # type: ignore

    return create_model(
        "DynamicResult",
        category=(literal_type, Field(description=f"Must be one of: {', '.join(classes)}")),
        reasoning=(str, Field(min_length=10, description="Explanation for classification")),
        __base__=BaseModel,
    )


async def classify(text: str, classes: list[str], domain: str = "category") -> Any:
    """Classify text into dynamically provided classes."""
    result_model = create_dynamic_classifier_model(classes)

    agent: Agent[None, Any] = Agent(
        "openai:gpt-5.2",
        output_type=result_model,
        system_prompt=f"Classify text into one of these {domain} categories: {', '.join(classes)}",
    )

    result = await agent.run(text)
    return result.output


# Usage
output = await classify(
    text="I can't believe they cancelled my flight without notice!",
    classes=["joy", "sadness", "anger", "fear", "neutral"],
    domain="emotion",
)
print(output.category)   # e.g. "anger"
print(output.reasoning)  # e.g. "The text expresses frustration and disbelief..."
```

## Running

```bash
cd dynamic_classification
uv run dynamic_classifier.py
```

## Output

```
Dynamic Classification with PydanticAI

Same code adapts to any number of classes at runtime

Example 1: 5-Way Emotion
Classes (5): ['joy', 'sadness', 'anger', 'fear', 'neutral']
Text: The movie was absolutely fantastic!

Result: joy
Reasoning: The text expresses strong enjoyment and enthusiasm, which maps to 'joy'
```

## Use Cases

- **Adaptable Systems** — Change classification categories without code changes
- **Multi-tenant Applications** — Different customers need different categories
- **A/B Testing** — Test different classification granularities
- **Domain-Specific Taxonomies** — Healthcare, legal, finance each have custom categories
- **User-Defined Categories** — Let users define their own classification schemes

## Why This Matters

!!! note "Traditional Approach"
    Traditional approaches require defining all possible classes upfront, recompiling/redeploying for new categories, and separate models for different granularities.

With dynamic Literals, you get:

- Runtime flexibility
- Type safety preserved
- Single codebase for all use cases
- Easy experimentation
