"""Example 4: History Filtering and Transformation

Demonstrates advanced history processing:
- Filter history to specific message types (user vs model)
- Understand ModelRequest (user) vs ModelResponse (model)
- Apply custom transformations before sending to agent
- Handle constraints (history must end with ModelRequest)

This example shows how to selectively use conversation history.
"""

import json

from dotenv import load_dotenv
from loguru import logger as log
from pydantic_ai import Agent, ModelMessage, ModelRequest, ModelResponse
from pydantic_ai.messages import ModelMessagesTypeAdapter

load_dotenv()


def user_message_filter(messages: list[ModelMessage]) -> list[ModelMessage]:
    """Filter history to only include user messages (ModelRequest).

    Args:
        messages: Full conversation history

    Returns:
        Only user messages from the conversation
    """
    return [msg for msg in messages if isinstance(msg, ModelRequest)]


def model_message_filter(messages: list[ModelMessage]) -> list[ModelMessage]:
    """Filter history to only include model responses (ModelResponse).

    Note: This will typically cause an error since history must end with
    a user message for the agent to process.

    Args:
        messages: Full conversation history

    Returns:
        Only model responses from the conversation
    """
    return [msg for msg in messages if isinstance(msg, ModelResponse)]


def main() -> None:
    """Run history filtering example."""
    # Load conversation history from previous example
    log.info("=== Loading Persisted History ===")
    save_path = "./output_3.json"
    with open(save_path, "rb") as f:
        conv = json.load(f)
    log.info("Historical conversation loaded")

    history = ModelMessagesTypeAdapter.validate_python(conv)

    # Example 1: Summarize only user messages
    log.info("\n=== Filtering: User Messages Only ===")
    agent_user = Agent("openai:gpt-4o", history_processors=[user_message_filter])
    result_1 = agent_user.run_sync("Please summarize the whole chat history until now.", message_history=history)
    log.info(f"Summary (user messages only):\n{result_1.output}")

    # Example 2: Attempt to filter only model messages (will fail)
    log.info("\n=== Filtering: Model Messages Only ===")
    agent_model = Agent("openai:gpt-4o", history_processors=[model_message_filter])
    try:
        result_2 = agent_model.run_sync("Please summarize the whole chat history until now.", message_history=history)
        log.info(f"Summary (model messages only):\n{result_2.output}")
    except Exception as e:
        log.error(f"Error: {e}")
        log.warning(
            "\nThis failed as expected! ⚠️\n"
            "History must end with a ModelRequest (user message) for\n"
            "the agent to process. Filtering to only ModelResponse\n"
            "messages violates this constraint."
        )


if __name__ == "__main__":
    main()
