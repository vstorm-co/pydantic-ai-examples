"""Example 5b: Dynamic Token-Based History Management

Demonstrates advanced, production-ready history management:
- Estimate tokens consumed by messages
- Dynamic context guarding based on thresholds
- Stateful processing with dataclasses and RunContext
- Trade-off: More complex but token-aware

This example shows professional patterns for managing context windows.
"""

import json
from dataclasses import dataclass

import tiktoken
from dotenv import load_dotenv
from loguru import logger as log
from pydantic_ai import Agent, ModelMessage, RunContext
from pydantic_ai.messages import ModelMessagesTypeAdapter

load_dotenv()

# `tiktoken` is used for OpenAI models, therefore if you're going to
# use different model provided, this bit will need to be changed
# to different tokenizer that corresponding to model used
tokenizer = tiktoken.encoding_for_model("gpt-4o")


@dataclass
class MemoryState:
    """Track token usage across conversation turns."""

    token_count: int = 0


def estimate_tokens(messages: list[ModelMessage]) -> int:
    """Estimate token count in messages using simple heuristic.

    Divides character count by 4 as rough approximation.
    For production, use proper tokenizer (e.g., tiktoken).

    Args:
        messages: List of messages to estimate tokens for

    Returns:
        Estimated token count
    """
    count = 0
    for message in messages:
        for msg in message.parts:
            count += len(tokenizer.encode(str(msg.content)))

    return count


# `context_guard()` below is an exemplary filter that allows to trim the
# number of messages persisting based on current token usage. For the sake
# of this example, threshold is set low for the logic to trigger. Usually,
# this value is much bigger and corresponds to used model's context
# window size. To fully utilize model processing capabilities it is best to
# set this value close to context size. For `gpt-4o` model this value is
# equal to 128_000 tokens


def context_guard(ctx: RunContext[MemoryState], messages: list[ModelMessage], token_threshold: int = 100) -> list[ModelMessage]:
    """Guard context size based on token usage.

    Trims history if token threshold exceeded.

    Args:
        ctx: Runtime context with memory state
        messages: Full conversation history
        token_threshold: Token limit before trimming

    Returns:
        Full history or trimmed version if threshold exceeded
    """
    current_token_usage = ctx.deps.token_count
    log.info(f"Current token usage: {current_token_usage}")

    if current_token_usage > token_threshold:
        log.info("Token threshold reached, trimming historical dialogue")
        return messages[-1:]
    return messages


def main() -> None:
    """Run dynamic token-based history example."""
    # Load conversation history from previous example
    log.info("=== Loading Persisted History ===")
    save_path = "./output_3.json"
    with open(save_path, "rb") as f:
        conv = json.load(f)
    log.info("Historical conversation loaded")

    ModelMessagesTypeAdapter.validate_python(conv)

    # Create state and agent with token-aware processor
    state = MemoryState()

    log.info("\n=== Agent with Dynamic Token-Based Context Guard ===")
    agent_2 = Agent(
        "openai:gpt-4o",
        deps_type=MemoryState,
        history_processors=[context_guard],
        system_prompt="You are a helpful and concise assistant.",
    )

    # First turn
    log.info("\n=== Turn 1 ===")
    result_2a = agent_2.run_sync("Tell me who you are", deps=state)
    log.info(f"Answer: {result_2a.output}")
    state.token_count += estimate_tokens(result_2a.all_messages())
    log.info(f"Tokens after turn 1: {state.token_count}")

    # Second turn
    log.info("\n=== Turn 2 ===")
    result_2b = agent_2.run_sync(
        "What are the most exceptional skills you posess? List at least 4 of them.",
        message_history=result_2a.all_messages(),
        deps=state,
    )
    log.info(f"Answer: {result_2b.output}")
    state.token_count += estimate_tokens(result_2a.all_messages())
    log.info(f"Tokens after turn 2: {state.token_count}")

    # Third turn
    log.info("\n=== Turn 3 ===")
    result_2c = agent_2.run_sync("What were we talking about??", message_history=result_2b.all_messages(), deps=state)
    log.info(f"Answer: {result_2c.output}")


if __name__ == "__main__":
    main()
