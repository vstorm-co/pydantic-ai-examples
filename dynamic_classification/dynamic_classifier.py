"""
Dynamic Classification with PydanticAI
Demonstrates runtime-adaptable classification with dynamic Literal types.
"""

from typing import Literal
from pydantic import BaseModel, Field, create_model
from pydantic_ai import Agent
from dotenv import load_dotenv

load_dotenv()


def create_dynamic_classifier(classes: list[str]) -> type[BaseModel]:
    """Dynamically create a Pydantic model with runtime-defined Literal classes."""
    literal_type = Literal[*tuple(classes)]  # type: ignore
    
    return create_model(
        "DynamicResult",
        category=(
            literal_type,
            Field(description=f"Must be one of: {', '.join(classes)}")
        ),
        reasoning=(
            str,
            Field(min_length=10, description="Explanation for classification")
        ),
        __base__=BaseModel,
    )


async def classify(text: str, classes: list[str], domain: str = "category") -> BaseModel:
    """Classify text into dynamically provided classes."""
    ResultModel = create_dynamic_classifier(classes)
    
    agent = Agent(
        "openai:gpt-4o-mini",
        output_type=ResultModel,
        system_prompt=f"Classify text into one of these {domain} categories: {', '.join(classes)}",
    )
    
    result = await agent.run(text)
    return result.output


EXAMPLES = [

    {
        "title": "5-Way Emotion",
        "text": "I can't believe they cancelled my flight without notice!",
        "classes": ["joy", "sadness", "anger", "fear", "neutral"],
        "domain": "emotion"
    },
    {
        "title": "Support Priority",
        "text": "My account has been hacked and I can't access my funds!",
        "classes": ["critical", "high", "medium", "low"],
        "domain": "priority"
    },
    {
        "title": "News Category",
        "text": "Scientists discover new exoplanet with potential for life.",
        "classes": ["science", "politics", "sports", "entertainment", "business", "technology"],
        "domain": "category"
    },
]


async def main():
    print("Dynamic Classification with PydanticAI\n")
    print("Same code adapts to any number of classes at runtime\n")
    print("=" * 70)
    
    for i, example in enumerate(EXAMPLES, 1):
        print(f"\nExample {i}: {example['title']}")
        print(f"Classes ({len(example['classes'])}): {example['classes']}")
        print(f"Text: {example['text']}")
        
        result = await classify(
            example["text"],
            example["classes"],
            example["domain"]
        )
        
        print(f"\nResult: {result.category}")
        print(f"Reasoning: {result.reasoning}")
        print("-" * 70)


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
