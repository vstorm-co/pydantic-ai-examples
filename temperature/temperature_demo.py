
from pydantic import BaseModel, Field
from pydantic_ai import Agent
from pydantic_ai.models import ModelSettings
from dotenv import load_dotenv

load_dotenv()


class StoryOpening(BaseModel):
    text: str = Field(description="Opening paragraph of a story")


async def test_temperature_creative_writing():
    """Demonstrate how temperature affects creative writing."""
    print("Temperature in Creative Writing\n")
    print("=" * 70)
    print("Prompt: Write the opening paragraph of a mystery novel\n")
    
    temperatures = [0.3, 0.8, 1.5]
    
    for temp in temperatures:
        agent = Agent(
            "openai:gpt-5.2",
            output_type=StoryOpening,
            model_settings=ModelSettings(temperature=temp),
        )
        
        result = await agent.run("Write the opening paragraph of a mystery novel set in a small coastal town.")
        
        print(f"Temperature: {temp}")
        print(f"Output:\n{result.output.text}\n")
        print("-" * 70)
    



async def main():
    print("\nModel Parameters: Temperature for Creative Writing\n")
    
    await test_temperature_creative_writing()


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
