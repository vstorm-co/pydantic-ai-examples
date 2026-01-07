# Reasoning Effort Parameter

Demonstrates the `reasoning_effort` parameter available in GPT-4o and o1 series models.

## Overview

The `reasoning_effort` parameter controls the depth of internal reasoning before generating output.

**Available Values:**
- `low`: Minimal reasoning steps, faster response
- `medium`: Balanced reasoning depth and speed
- `high`: Maximum reasoning depth, thorough analysis

## Technical Details

This parameter affects:
- Number of internal reasoning tokens generated
- Verification steps performed before output
- Trade-off between latency and solution quality

## Implementation

```python
from pydantic_ai.models import ModelSettings

agent = Agent(
    "openai:gpt-4o",
    model_settings=ModelSettings(reasoning_effort="high")
)
```

## Running

```bash
cd reasoning_effort
uv run reasoning_demo.py
```

## Use Cases

| Reasoning Effort  Best For |
|-----------------|----------|
| low  | Simple queries, quick responses |
| medium  | General problem-solving |
| high | Complex math, logic, planning |

## Task Types

**High Reasoning Effort:**
- Mathematical proofs
- Multi-step logic problems
- Code debugging and optimization
- Strategic planning (TSP, scheduling)
- Theorem proving

**Medium Reasoning Effort:**
- Data analysis
- Code generation
- Technical explanations
- Decision making

**Low Reasoning Effort:**
- Simple calculations
- Factual queries
- Quick assistance
- Classification

## Model Availability
- Make sure chosen model supports reasoning effort 

## Performance Impact

**Latency:**
```
low:    1.2x baseline
medium: 2.0x baseline  
high:   3.5x baseline
```

**Token Usage:**
- Reasoning tokens are generated internally but not counted toward output
- Check OpenAI pricing for reasoning token costs

## Example Output

**Problem:** A farmer has chickens and rabbits. 35 heads, 94 legs. How many of each?

**Low Reasoning:**
```
Answer: 23 chickens, 12 rabbits
Reasoning: Using x + y = 35 and 2x + 4y = 94, solving gives x = 23, y = 12
```

**High Reasoning:**
```
Answer: 23 chickens, 12 rabbits
Reasoning: Let x = chickens, y = rabbits.
Constraint 1: x + y = 35 (total heads)
Constraint 2: 2x + 4y = 94 (total legs)
From Constraint 1: x = 35 - y
Substitute into Constraint 2: 2(35 - y) + 4y = 94
Simplify: 70 - 2y + 4y = 94
Solve: 2y = 24, y = 12
Therefore: x = 35 - 12 = 23
Verification: 23 + 12 = 35 ✓, 2(23) + 4(12) = 46 + 48 = 94 ✓
```
