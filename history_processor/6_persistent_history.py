"""Example 6: Persistent History with Database Storage

Demonstrates production-ready conversation persistence:
- Save conversation history to SQLite database
- Store prompts, responses, and metadata
- Retrieve and query historical conversations
- Track token usage and model information
- Build a persistent conversation archive

This example shows how to build durable conversation storage systems.
"""

from typing import List

from dotenv import load_dotenv
from icecream import ic
from loguru import logger as log
from pydantic_ai import Agent, AgentRunResult
from sqlalchemy import Text, create_engine
from sqlalchemy.orm import Mapped, declarative_base, mapped_column, sessionmaker
from sqlalchemy.types import JSON

load_dotenv()


# --- Database Setup ---
engine = create_engine(
    "sqlite:///mydb.db",
    connect_args={"autocommit": False}
)
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)
Base = declarative_base()
db = SessionLocal()


class ConversationRecord(Base):
    """Database model for storing conversation records.

    Attributes:
        id: Unique identifier for the record
        question: User prompt/question
        answer: Agent response
        model_used: Model identifier (e.g., "gpt-4o")
        usage: Token usage metadata (input, output, total tokens)
    """

    __tablename__ = "conversations"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    question: Mapped[str] = mapped_column(Text, default="")
    answer: Mapped[str] = mapped_column(Text, default="")
    model_used: Mapped[str] = mapped_column(Text, default="")
    usage: Mapped[JSON] = mapped_column(JSON, default={})


Base.metadata.create_all(bind=engine)


def prepare_data_for_db(
    prompt: str,
    result: AgentRunResult
) -> ConversationRecord:
    """Convert agent result to database record.

    Args:
        prompt: User question/prompt
        result: Agent execution result

    Returns:
        ConversationRecord ready for database insertion
    """
    return ConversationRecord(
        question=prompt,
        answer=result.output,
        model_used=result.all_messages()[-1].model_name,
        usage=result.usage().__dict__
    )


def add_message_to_db(record: ConversationRecord) -> None:
    """Persist conversation record to database.

    Args:
        record: ConversationRecord to save
    """
    db.add(record)
    db.commit()
    log.info(f"Conversation saved to database with ID: {record.id}")


def get_all_conversations() -> List[ConversationRecord]:
    """Retrieve all conversations from database.

    Returns:
        List of all conversation records
    """
    conversations = db.query(ConversationRecord).all()
    return conversations


def get_conversation_by_id(record_id: int) -> ConversationRecord | None:
    """Retrieve specific conversation by ID.

    Args:
        record_id: Database record ID

    Returns:
        ConversationRecord if found, None otherwise
    """
    return db.query(ConversationRecord).filter(
        ConversationRecord.id == record_id
    ).first()


def main() -> None:
    """Run database persistence example."""
    # Initialize agent
    log.info("=== Initializing Agent ===")
    agent = Agent(
        "openai:gpt-4o",
        system_prompt=(
            "You are a helpful assistant. Respond concisely and clearly."
        )
    )

    # Run conversation and save to database
    log.info("\n=== Running Conversation ===")
    prompt = "What are the three key benefits of learning Python?"
    result = agent.run_sync(user_prompt=prompt)
    log.info(f"Prompt: {prompt}")
    log.info(f"Answer: {result.output}")

    # Save to database
    log.info("\n=== Saving to Database ===")
    record = prepare_data_for_db(prompt, result)
    add_message_to_db(record)

    # Retrieve and display all conversations
    log.info("\n=== All Conversations in Database ===")
    conversations = get_all_conversations()
    log.info(f"Total conversations: {len(conversations)}")

    for conv in conversations:
        ic(conv.__dict__)


if __name__ == "__main__":
    main()
    
    
    

