# Pydantic AI Examples

A comprehensive collection of examples demonstrating Pydantic AI's features and best practices.

## 📁 Examples

### [History Processor](./history_processor/README.md)

Learn how to manage conversation history in AI agents:

- Basic history handling and inspection
- Multi-turn conversations with context
- History persistence (JSON and Database)
- Advanced filtering and transformation
- Context window management strategies
- Production-ready database archival

**Getting started:** `cd history_processor && uv run python 1_basic_history_handling.py`

See [history_processor/README.md](./history_processor/README.md) for detailed walkthrough of all 6 examples.

## 🛠️ Setup

```bash
# Move into dir
cd history_processor

# Install dependencies
uv sync

# Configure environment
cp history_processor/.env.example history_processor/.env

# Edit .env and add your OpenAI API key (i.ex. with `nano`)
nano .env
```

## 📚 Learning Path

1. Start with [history_processor](./history_processor/README.md) - foundational concepts
2. Explore advanced patterns as you progress through examples
3. Use examples as templates for your own projects

## 🔗 Resources

- [Pydantic AI Documentation](https://ai.pydantic.dev/)
- [Python Documentation](https://docs.python.org/)
