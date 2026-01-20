"""Example 5c: History Trimming with Tool Calls

Demonstrates history-processing strategies that preserve tool-call / tool-response integrity.

- `keep_last_messages`: simple N-message truncation
- `keep_last_messages_with_tools`: truncation that attempts to keep tool call/response pairs

This example attaches a simple tool to an `Agent` and demonstrates multi-turns
with message history. It highlights pitfalls when history slicing breaks
tool-call completeness.

Usage:
    uv run python 5c_history_with_tools.py
"""

import secrets
from collections.abc import Callable

from dotenv import load_dotenv
from icecream import ic
from loguru import logger as log
from pydantic_ai import Agent, ModelMessage, ModelRequest, RunContext, ToolReturnPart

load_dotenv()


def keep_last_messages(messages: list[ModelMessage], num_messages: int = 3) -> list[ModelMessage]:
    """Keep only the last N messages from history.

    Args:
        messages: Full conversation history
        num_messages: Number of messages to retain

    Returns:
        Last num_messages from the conversation, or all if fewer exist
    """
    log.info(f"Current message count: {len(messages)}")
    log.info(f"Filtering for last {num_messages} messages in the conversation")
    output = messages[-num_messages:] if len(messages) > num_messages else messages
    return output


def keep_last_messages_with_tools(messages: list[ModelMessage], num_messages: int = 3) -> list[ModelMessage]:
    """Keep only the last N messages from history, preserving tool-call/response pairs.

    Unlike `keep_last_messages`, this processor carefully preserves tool-call and
    tool-response pairs to avoid breaking the agent's tool execution flow.

    Args:
        messages: Full conversation history with tool calls
        num_messages: Number of messages to retain

    Returns:
        Last num_messages from the conversation, or all if fewer exist
    """
    log.info(f"Current message count: {len(messages)}")
    log.info(f"Filtering for last {num_messages} messages in the conversation including tool calls")

    # Check if cutting is needed
    if len(messages) <= num_messages:
        return messages

    start_index = -num_messages

    # Ensure we don't split a tool-call/response pair by checking if the boundary
    # falls in the middle of a tool interaction. If so, move the start index back.
    first_msg = messages[start_index]

    if isinstance(first_msg, ModelRequest) and any(isinstance(part, ToolReturnPart) for part in first_msg.parts):
        start_index -= 1

    # Ensure we do not go out of bounds
    return messages[max(-len(messages), start_index) :]


def run_conversation_with_history_processor(history_processor: Callable[..., list[ModelMessage]]) -> None:
    processor_name = getattr(history_processor, "__name__", "unknown_processor")
    log.info(f"\n=== Running with history processor: {processor_name} ===")

    # Create agent with history processor
    agent = Agent("openai:gpt-5.1", system_prompt="You are a helpful and playful assistant", history_processors=[history_processor])

    # Add basic tool
    @agent.tool
    async def throw_dice(ctx: RunContext[None]) -> int:
        "Roll a die and return a random number between 1 and 6"
        return secrets.choice([1, 2, 3, 4, 5, 6])

    try:
        result_1 = agent.run_sync("Please provide a random number")
        ic(result_1.output)

        result_2 = agent.run_sync("Okay, let's do this one more time!", message_history=result_1.all_messages())
        ic(result_2.output)

        # Display full conversation history
        log.info(f"\nTotal messages in history: {len(result_2.all_messages())}")
        for idx, msg in enumerate(result_2.all_messages(), start=1):
            # Extract readable message content; parts may vary in type
            content = getattr(msg.parts[0], "content", str(msg.parts)) if msg.parts else "(no content)"
            log.info(f"Message #{idx}: {content}")

    except Exception as e:
        log.error(f"Agent failed: {e}")
        log.warning(
            "\nThis failure demonstrates a key lesson! ⚠️\n"
            "When history slicing splits a tool-call / tool-response pair (e.g., cuts "
            "the response but keeps the call), the agent cannot continue and raises an error.\n"
            "This is why `keep_last_messages_with_tools` exists: to avoid this pitfall."
        )


def main() -> None:
    """Run message count example with tool usage."""

    log.info("Run basic history trimming method with tool calls")
    run_conversation_with_history_processor(keep_last_messages)

    log.info("Run tool optimized trimming method with tool calls")
    run_conversation_with_history_processor(keep_last_messages_with_tools)


if __name__ == "__main__":
    main()
