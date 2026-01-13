"""Example 5a: Fixed Message Count History Management

Demonstrates simple history truncation strategies:
- Keep only the last N messages
- Basic approach for preventing history bloat
- Useful for simple use cases with small context windows
- Trade-off: May lose important context

This example shows a straightforward fixed-window approach.
"""

import json

from dotenv import load_dotenv
from loguru import logger as log
from pydantic_ai import Agent, ModelMessage
from pydantic_ai.messages import ModelMessagesTypeAdapter

load_dotenv()


def keep_last_messages(messages: list[ModelMessage], num_messages: int = 3) -> list[ModelMessage]:
    """Keep only the last N messages from history.

    Args:
        messages: Full conversation history
        num_messages: Number of messages to retain

    Returns:
        Last num_messages from the conversation, or all if fewer exist
    """
    log.info(f"Filtering for last {num_messages} messages in the conversation")
    output = messages[-num_messages:] if len(messages) > num_messages else messages
    return output


def main() -> None:
    """Run fixed message count history example."""
    # Load conversation history from previous example
    log.info("=== Loading Persisted History ===")
    with open("output_3.json", "rb") as f:
        conv = json.load(f)
    log.info("Historical conversation loaded")

    history = ModelMessagesTypeAdapter.validate_python(conv)
    log.info(f"Total messages in history: {len(history)}")

    # Create agent with message count limiter
    log.info("\n=== Agent with Fixed Message Limit (last 3) ===")
    agent_1 = Agent("openai:gpt-4o", history_processors=[keep_last_messages])
    result_1 = agent_1.run_sync("What were we talking about?", message_history=history)
    log.info(f"Answer (with truncated history):\n{result_1.output}")


if __name__ == "__main__":
    main()
