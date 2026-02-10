# Dynamic Classification

Runtime-adaptable classification using dynamically generated Literal types.

## Overview

This example demonstrates how to build a classifier that adapts to **any number of classes** at runtime, using Pydantic's `create_model()` to generate dynamic Literal types.

## Key Technique

```python
def create_dynamic_classifier(classes: list[str]) -> type[BaseModel]:
    literal_type = Literal[tuple(classes)]  # Dynamic Literal!

    return create_model(
        "DynamicResult",
        category=(literal_type, Field(description="Chosen category")),
        reasoning=(str, Field(description="Model reasoning", min_length=1)),
        __base__=BaseModel,
    )
```

## Running

```bash
cd dynamic_classification
uv run dynamic_classifier.py
```

## Output

```zsh
Dynamic Classification with PydanticAI

Same code adapts to any number of classes at runtime

Example 1: 5-Way Emotion
Classes (5): ['joy', 'sadness', 'anger', 'fear', 'neutral']
Text: The movie was absolutely fantastic!

Result: joy
Reasoning: The text expresses strong enjoyment and enthusiasm, which maps to 'joy'
```

## Use Cases

- **Adaptable Systems**: Change classification categories without code changes
- **Multi-tenant Applications**: Different customers need different categories
- **A/B Testing**: Test different classification granularities
- **Domain-Specific Taxonomies**: Healthcare, legal, finance each have custom categories
- **User-Defined Categories**: Let users define their own classification schemes

## Why This Matters

Traditional approaches require:

1. Defining all possible classes upfront
2. Recompiling/redeploying for new categories
3. Separate models for different granularities

With dynamic Literals, you get:

- Runtime flexibility
- Type safety preserved
- Single codebase for all use cases
- Easy experimentation
