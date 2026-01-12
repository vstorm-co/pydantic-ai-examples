"""
Basic Sentiment Classification with PydanticAI
Fixed 3-class sentiment analysis with structured outputs.
"""

from typing import Literal
from pydantic import BaseModel, Field
from pydantic_ai import Agent
from dotenv import load_dotenv

load_dotenv()


REVIEWS = [
    ("This product is absolutely amazing! Best purchase ever!", "positive"),
    ("Terrible quality, broke after one day. Very disappointed.", "negative"),
    ("It's okay, nothing special but does the job.", "neutral"),
    ("I love this! Exceeded all my expectations.", "positive"),
    ("Waste of money. Do not recommend at all.", "negative"),
    ("The product works as advertised. No complaints.", "neutral"),
    ("Outstanding quality and fast shipping!", "positive"),
]


class SentimentResult(BaseModel):
    sentiment: Literal["positive", "negative", "neutral"] = Field(
        description="The sentiment category of the text"
    )
    reasoning: str = Field(
        min_length=10,
        description="Brief explanation for the sentiment classification"
    )


sentiment_agent = Agent(
    "openai:gpt-5.2",
    output_type=SentimentResult,
    retries=0,
    system_prompt=(
        "You are a sentiment analysis expert. Classify the given text as "
        "positive, negative, or neutral. Provide brief reasoning for your classification."
    ),
)



async def main():
    print("Sentiment Analysis with PydanticAI\n")
    print("=" * 70)
    
    correct = 0
    total = len(REVIEWS)
    
    for i, (text, expected) in enumerate(REVIEWS, 1):
        print(f"\nReview {i}/{total}:")
        print(f"Text: {text}")
        
        result = await sentiment_agent.run(text)
        output = result.output
        
        print(f"\nClassification:")
        print(f"  Sentiment: {output.sentiment}")
        print(f"  Reasoning: {output.reasoning}")
        print(f"  Expected: {expected}")
        
        if output.sentiment == expected:
            correct += 1
            print("  Status: Correct")
        else:
            print("  Status: Incorrect")
        
        print("-" * 70)
    
    accuracy = (correct / total) * 100
    print(f"\nResults: {correct}/{total} correct ({accuracy:.1f}% accuracy)")


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
