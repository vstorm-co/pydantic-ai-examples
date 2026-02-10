---
title: Temperature
---

# Temperature

Demonstrates temperature parameter control in language model generation.

## What is Temperature?

Temperature controls output randomness by scaling logits before softmax sampling:

```
P(token_i) = exp(logit_i / T) / Σ exp(logit_j / T)
```

Where T = temperature value:

- **T → 0**: Distribution approaches argmax (deterministic)
- **T = 1**: Unchanged probability distribution
- **T > 1**: Flattened distribution (more uniform sampling)

## Implementation

```python
from pydantic_ai import Agent
from pydantic_ai.models import ModelSettings

agent = Agent(
    "openai:gpt-4.1",
    model_settings=ModelSettings(temperature=0.3)
)
```

## Running

```bash
cd temperature
uv run temperature_demo.py
```

## Example Output

**Same prompt: "Write the opening paragraph of a mystery novel"**

```
Temperature: 0.3
The fog rolled in thick from the ocean, wrapping the small coastal town
in a shroud of gray. Streetlamps flickered, casting eerie shadows on
cobblestone streets. The clock struck midnight, and a piercing scream
shattered the stillness.

Temperature: 0.8
On the rugged cliffs of Seabreeze Cove, where the ocean's roar battled
against whispers of the past, the air was thick with secrets. When the
lighthouse keeper was found dead, the tranquil facade began to crack.

Temperature: 1.5
The town of Brackley Point had always seemed ordinary, with weathered
wooden buildings and peeling paint beneath relentless coastal winds. But
as dusk fell, an unexpected chill crept in—not from the ocean, but from
secrets buried deep within the town's foundations.
```

## Temperature Values

| Value | Effect | Token Selection |
|-------|--------|----------------|
| 0.0–0.3 | Low entropy | Top-1 to top-3 tokens dominate |
| 0.7–1.0 | Moderate entropy | Balanced probability distribution |
| 1.5–2.0 | High entropy | Broader token sampling range |

!!! warning "Reasoning Models Do Not Support Temperature"
    OpenAI reasoning models (e.g. `gpt-5`, `gpt-5-mini`, `gpt-5-nano`, `o3`) do not support the `temperature`, `top_p`, or `logprobs` parameters. Requests to these models that include these fields will raise an error.

    **Exception:** `gpt-5.2` and `gpt-5.1` support `temperature`, `top_p`, and `logprobs` **only** when reasoning effort is set to `none`.

    For reliable temperature control, use non-reasoning models like `gpt-4.1`.

    See the [OpenAI API docs](https://developers.openai.com/api/docs/guides/latest-model) and the [community discussion](https://community.openai.com/t/gpt-5-models-temperature/1337957/5) for more details.

## Use Cases by Task Type

!!! tip "Deterministic Tasks (T = 0.0–0.3)"
    Classification, data extraction, code generation, factual queries.

!!! tip "Generative Tasks (T = 0.7–1.0)"
    Conversational responses, content writing, general assistance.

!!! tip "Creative Tasks (T = 1.2–2.0)"
    Fiction writing, brainstorming, idea generation.
