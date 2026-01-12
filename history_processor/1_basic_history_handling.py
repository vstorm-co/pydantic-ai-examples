"""Example 1: Basic History Handling

Demonstrates how to inspect and access conversation history in different formats:
- View history as JSON
- Access individual message objects
- Understand ModelMessage structure

This is a foundational example showing how history is stored and accessed.
"""

from dotenv import load_dotenv
from icecream import ic
from loguru import logger as log
from pydantic_ai import Agent

load_dotenv()


def main() -> None:
    """Run basic history inspection example."""
    # Create a basic agent
    agent = Agent(
        model="openai:gpt-4o",
        system_prompt="Be a helpful assistant"
    )

    # Run a single inference
    prompt = "Tell me a funny joke. Respond in plain text."
    result = agent.run_sync(prompt)
    log.info(f"\nPrompt: {prompt}\nAnswer: {result.output}")

    # Inspect history as JSON
    log.info("\n=== History as JSON ===")
    history_json = result.all_messages_json().decode("utf-8")
    ic(history_json)

    # Inspect individual message objects
    log.info("\n=== History as Objects ===")
    for idx, message in enumerate(result.all_messages()):
        log.info(f"Message #{idx + 1}: {type(message).__name__}")
        ic(message)


if __name__ == "__main__":
    main()
