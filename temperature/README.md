# Model Parameters

Demonstrates temperature parameter control in language model generation.

## Temperature

Temperature controls output randomness by scaling logits before softmax sampling.

**Mathematical base:**

```
P(token_i) = exp(logit_i / T) / Σ exp(logit_j / T)
```

Where T = temperature value.

- **T → 0**: Distribution approaches argmax (deterministic)
- **T = 1**: Unchanged probability distribution
- **T > 1**: Flattened distribution (more uniform sampling)

## Implementation

```python
from pydantic_ai.models import ModelSettings

agent = Agent(
    "openai:gpt-4o-mini",
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
The fog rolled in thick from the ocean, wrapping the small coastal town in a shroud of gray.
Streetlamps flickered, casting eerie shadows on cobblestone streets. The clock struck midnight,
and a piercing scream shattered the stillness.

Temperature: 0.8
On the rugged cliffs of Seabreeze Cove, where the ocean's roar battled against whispers of
the past, the air was thick with secrets. When the lighthouse keeper was found dead, the
tranquil facade began to crack.

Temperature: 1.5
The town of Brackley Point had always seemed ordinary, with weathered wooden buildings and
peeling paint beneath relentless coastal winds. But as dusk fell, an unexpected chill crept
in—not from the ocean, but from secrets buried deep within the town's foundations.
```

## Temperature Values

| Value | Effect | Token Selection |
|-------|--------|----------------|
| 0.0-0.3 | Low entropy | Top-1 to top-3 tokens dominate |
| 0.7-1.0 | Moderate entropy | Balanced probability distribution |
| 1.5-2.0 | High entropy | Broader token sampling range |

## Use Cases by Task Type

**Deterministic Tasks (T = 0.0-0.3)**
- Classification
- Data extraction
- Code generation
- Factual queries

**Generative Tasks (T = 0.7-1.0)**
- Conversational responses
- Content writing
- General assistance

**Creative Tasks (T = 1.2-2.0)**
- Fiction writing
- Brainstorming
- Idea generation
