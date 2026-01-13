"""Example 3: History Usage in Real-World Workflows

Demonstrates practical history applications:
- Building realistic multi-turn conversations
- Leveraging history for conversation summarization
- Persisting history to JSON for later use
- Loading persisted conversations

This example shows production-ready patterns for history management.
"""

from dotenv import load_dotenv
from icecream import ic
from loguru import logger as log
from pydantic_ai import Agent
from pydantic_ai.messages import ModelMessage

load_dotenv()


def main() -> None:
    """Run multi-turn conversation with persistence example."""
    # Create agent
    agent = Agent(model="openai:gpt-4o", system_prompt="Be a helpful assistant")

    # Turn 1: Get initial motto
    log.info("\n=== Turn 1 ===")
    result_1 = agent.run_sync("Provide me with a good motto for today!")
    log.info(f"Answer: {result_1.output}")

    # Turn 2: Explain the choice
    log.info("\n=== Turn 2 ===")
    result_2 = agent.run_sync("Why did you choose this one? Please explain it a bit more.", message_history=result_1.all_messages())
    log.info(f"Answer: {result_2.output}")

    # Turn 3: Request another motto
    log.info("\n=== Turn 3 ===")
    result_3 = agent.run_sync("Wow, thanks a lot! How about another one for my friend?", message_history=result_2.all_messages())
    log.info(f"Answer: {result_3.output}")

    # Turn 4: Summarize conversation
    log.info("\n=== Turn 4: Summarization ===")
    summary_prompt = (
        "Please summarize the whole conversation until this message. "
        "Point out key topics and provide a timeline of events from this conversation."
    )
    result_4 = agent.run_sync(summary_prompt, message_history=result_3.all_messages())
    log.info(f"Summary: {result_4.output}")

    # Inspect full history
    log.info("\n=== Complete History ===")
    history: list[ModelMessage] = result_4.all_messages()
    log.info(f"Total messages: {len(history)}")
    for idx, message in enumerate(history):
        log.info(f"\nMessage #{idx + 1}: {type(message).__name__}")
        ic(message)

    # Persist history for use in example 4
    log.info("\n=== Saving to File ===")
    history_json = result_4.all_messages_json()
    save_path = "./output_3.json"
    with open(save_path, "wb") as f:
        f.write(history_json)
    log.info(f"History saved to {save_path}")


if __name__ == "__main__":
    main()
