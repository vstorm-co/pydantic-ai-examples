---
title: Reasoning Effort
---

# Reasoning Effort

## Overview

Reasoning models like GPT-5, GPT-5-mini, and GPT-5-nano are LLMs trained with reinforcement learning to perform complex problem-solving. They **"think before they answer"** — producing internal chains of thought (reasoning tokens) before generating the visible response. These models excel at coding, scientific reasoning, and multi-step planning tasks.

The `reasoning_effort` parameter controls how many reasoning tokens the model generates internally, letting you tune the trade-off between response speed/cost and solution quality.

**Available values:**

| Value | Description |
|---|---|
| `low` | Favors speed and economical token usage |
| `medium` | Balances speed and reasoning accuracy (default for reasoning models) |
| `high` | Prioritizes complete, thorough reasoning over speed |

GPT-5.2 additionally supports `none` (no internal reasoning, lowest latency) and `xhigh` (maximum reasoning depth).

For full details, see the official OpenAI documentation:

- [Reasoning models guide](https://developers.openai.com/api/docs/guides/reasoning)
- [Latest model overview (GPT-5.2)](https://developers.openai.com/api/docs/guides/latest-model)

## How Reasoning Tokens Work

When a reasoning model processes a request, it generates **reasoning tokens** internally before producing the final answer. Key characteristics:

- **Not visible** in the API response, but they occupy context window space
- **Billed as output tokens** — check [OpenAI pricing](https://openai.com/api/pricing/) for reasoning token costs
- **Token count** is available in `usage.output_tokens_details` in the response
- Can range from **hundreds to tens of thousands** of tokens per request depending on problem complexity and effort level
- **Discarded** after the final answer is generated (not cached between turns)

!!! tip "Context Budget"
    Reserve at least **25,000 tokens** for reasoning and outputs when experimenting. Use `max_output_tokens` to control costs. If a response hits the limit before producing output, the finish reason will be `max_output_tokens`.

## Code Example

This example from the repo demonstrates comparing reasoning effort levels using PydanticAI with the OpenAI Responses API:

```python
from pydantic import BaseModel, Field
from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIResponsesModelSettings, ReasoningEffort


class Solution(BaseModel):
    answer: str = Field(description="Solution to the problem")


async def test_reasoning_effort():
    """Compare reasoning effort levels on a complex problem."""
    problem = """
    A farmer has chickens and rabbits. There are 35 heads and 94 legs total.
    How many chickens and how many rabbits are there?
    """

    efforts: list[ReasoningEffort] = ["low", "medium", "high"]

    for effort in efforts:
        agent: Agent[None, Solution] = Agent(
            "openai:gpt-5.2",
            output_type=Solution,
            model_settings=OpenAIResponsesModelSettings(
                openai_reasoning_effort=effort,
                openai_reasoning_summary="detailed",
            ),
        )

        result = await agent.run(f"Solve this problem:\n{problem}")

        print(f"Reasoning Effort: {effort}")
        print(f"Answer: {result.output.answer}")
```

Key settings in `OpenAIResponsesModelSettings`:

- **`openai_reasoning_effort`** — controls reasoning depth (`"low"`, `"medium"`, `"high"`)
- **`openai_reasoning_summary`** — set to `"detailed"` to get a summary of the model's internal reasoning chain

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

## Running

```bash
cd reasoning_effort
uv run reasoning_demo.py
```

## Use Cases

### High Reasoning Effort

Best for tasks where accuracy matters more than speed:

- Mathematical proofs and multi-step logic problems
- Complex code debugging and optimization
- Strategic planning (TSP, scheduling, resource allocation)
- Scientific reasoning and analysis

### Medium Reasoning Effort

Good default for general-purpose tasks:

- Data analysis and interpretation
- Code generation
- Technical explanations

### Low Reasoning Effort

Use when speed and cost matter more than depth:

- Simple calculations and factual queries
- Classification and categorization
- Quick lookups and straightforward assistance

## Prompting Tips for Reasoning Models

Reasoning models work differently from standard GPT models. OpenAI recommends treating them like an **experienced colleague** rather than giving explicit step-by-step instructions:

- **Keep prompts high-level** — describe the goal, not the individual steps. The model's internal reasoning handles the decomposition.
- **Avoid chain-of-thought prompts** — phrases like "think step by step" are unnecessary and can actually degrade performance since the model already reasons internally.
- **Use delimiters** for clarity — triple quotes, XML tags, or markdown headers help the model parse complex inputs.
