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
    """Keep only the last N messages from history including tool calls.

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

    # Check tool sequence integrity
    first_msg = messages[start_index]

    if isinstance(first_msg, ModelRequest) and any(isinstance(part, ToolReturnPart) for part in first_msg.parts):
        start_index -= 1

    # Ensure we do not go out of bounds
    return messages[max(-len(messages), start_index) :]


def run_conversation_with_history_processor(history_processor: Callable) -> None:
    log.info("\n=== Agent with Fixed Message Limit with tools ===")
    log.info(f"\n=== Used history processor: {getattr(history_processor, '__name__', 'unknown_processor')} ===")

    # Create agent with history processor
    agent = Agent("openai:gpt-4o", system_prompt="You are a helpful and playful assistant", history_processors=[history_processor])

    # Add basic tool
    @agent.tool
    async def throw_dice(ctx: RunContext[None]) -> int:
        "Throws a dice to get a random number between 1 and 6"
        return secrets.choice([1, 2, 3, 4, 5, 6])

    try:
        result_1 = agent.run_sync("Please provide a random number")
        ic(result_1.output)
        ic(result_1.all_messages())

        result_2 = agent.run_sync("Okay, let's do this one more time!", message_history=result_1.all_messages())
        ic(result_2.output)

        # Iterate over history
        for idx, msg in enumerate(result_2.all_messages()):
            log.info(f"\nMessage no {idx}\nMessage content: {msg.parts[0].content if hasattr(msg.parts[0], 'content') else msg.parts}")

    except Exception as e:
        log.info(f"Error: {e}")
        log.warning(
            "\nThis failed as expected! ⚠️\n"
            "History must include complete tool calls being ToolCallPart and "
            "ToolResponsePart. If some dangling ones will remain, as in this case "
            "you'll end up with and error."
        )


def main() -> None:
    """Run message count example with tool usage."""

    log.info("Run basic history trimming method with tool calls")
    run_conversation_with_history_processor(keep_last_messages)

    log.info("Run tool optimized trimming method with tool calls")
    run_conversation_with_history_processor(keep_last_messages_with_tools)


if __name__ == "__main__":
    main()
