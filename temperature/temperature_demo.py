from dotenv import load_dotenv
from pydantic import BaseModel, Field
from pydantic_ai import Agent
from pydantic_ai.models import ModelSettings

load_dotenv()


class StoryOpening(BaseModel):
    text: str = Field(description="Opening paragraphs of a story")


async def test_temperature_creative_writing():
    """Demonstrate how temperature affects creative writing."""
    prompt = "Write few opening paragraphs of a mystery novel set in a small coastal town."
    print("Temperature in Creative Writing\n")
    print("=" * 70)
    print(f"Prompt: {prompt}\n")

    temperatures = [0.3, 0.8, 1.5]

    for temp in temperatures:
        agent = Agent[None, StoryOpening](
            "openai:gpt-5.2",
            output_type=StoryOpening,
            model_settings=ModelSettings(temperature=temp),
        )

        result = await agent.run(prompt)

        print(f"Temperature: {temp}")
        print(f"Output:\n{result.output.text}\n")
        print("-" * 70)


async def main():
    print("\nModel Parameters: Temperature for Creative Writing\n")

    await test_temperature_creative_writing()


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
