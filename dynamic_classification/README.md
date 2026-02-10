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

### Typed Version with Enums and Protocols

For better typing and IDE support, use dynamic Enums with Protocol type hints. Under the hood PydanticAI sends literals as enums, so while more verbose it's more reflective of the actual data.

```python
from enum import Enum
from typing import Protocol

class ClassificationResult(Protocol):
    """Protocol defining the structure of classification results."""
    category: Enum
    reasoning: str

def create_dynamic_classifier_model(classes: list[str]) -> type[ClassificationResult]:
    """Dynamically create a Pydantic model with runtime-defined Enum classes."""
    output_type = Enum("OutputClass", {cls: cls for cls in classes})

    return create_model(
        "DynamicResult",
        category=(output_type, Field(description=f"Must be one of: {', '.join(classes)}")),
        reasoning=(str, Field(min_length=10, description="Explanation for classification")),
        __base__=BaseModel,
    )
```

This approach provides:

- **Type safety**: Return type clearly indicates the structure via Protocol
- **IDE support**: Autocomplete for `category` and `reasoning` fields
- **Structured types**: Enum is a first-class type with additional functionality

## Running

```bash
cd dynamic_classification
uv run dynamic_classifier.py
```

or

```bash
cd dynamic_classification
uv run dynamic_classifier_typed.py
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
