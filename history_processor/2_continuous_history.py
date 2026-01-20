"""Example 2: Continuous History in Multi-Turn Conversations

Demonstrates maintaining context across multiple agent calls:
- Build multi-turn conversations with history
- Understand message_history parameter
- Difference between new_messages() and all_messages()
- Inspect full conversation state

This example shows the fundamental pattern for stateful conversations.
"""

from dotenv import load_dotenv
from icecream import ic
from loguru import logger as log
from pydantic_ai import Agent
from pydantic_ai.messages import ModelMessage

load_dotenv()


def main() -> None:
    """Run multi-turn conversation example."""
    # Create agent
    agent = Agent(model="openai:gpt-5.1", system_prompt="Be a helpful assistant")

    # First turn: Agent generates a joke
    prompt_1 = "Provide a really, really funny joke. Respond in plain text."
    result_1 = agent.run_sync(prompt_1)
    log.info("\n=== Turn 1 ===")
    log.info(f"Prompt: {prompt_1}")
    log.info(f"Answer: {result_1.output}")

    # Second turn: Pass history to context for follow-up
    # Using new_messages() to pass only messages from first inference
    prompt_2 = "I didn't get it. Care to explain?"
    result_2 = agent.run_sync(prompt_2, message_history=result_1.new_messages())
    log.info("\n=== Turn 2 ===")
    log.info(f"Prompt: {prompt_2}")
    log.info(f"Answer: {result_2.output}")

    # Inspect full conversation history
    log.info("\n=== Complete Conversation History ===")
    history: list[ModelMessage] = result_2.all_messages()
    log.info(f"Total messages: {len(history)}")
    for idx, message in enumerate(history):
        log.info(f"\nMessage #{idx + 1}: {type(message).__name__}")
        ic(message)


if __name__ == "__main__":
    main()
