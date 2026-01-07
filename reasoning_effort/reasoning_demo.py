from pydantic import BaseModel, Field
from pydantic_ai import Agent
from pydantic_ai.models import ModelSettings
from dotenv import load_dotenv

load_dotenv()


class Solution(BaseModel):
    answer: str = Field(description="Solution to the problem")
    reasoning: str = Field(description="Step-by-step reasoning process")


async def test_reasoning_effort():
    """Compare reasoning effort levels on a complex problem."""
    print("Reasoning Effort Parameter Comparison\n")
    print("=" * 70)
    
    problem = """
    A farmer has chickens and rabbits. There are 35 heads and 94 legs total.
    How many chickens and how many rabbits are there?
    """
    
    print(f"Problem: {problem.strip()}\n")
    
    efforts = ["low", "medium", "high"]
    
    for effort in efforts:
        agent = Agent(
            "openai:gpt-4o",
            output_type=Solution,
            model_settings=ModelSettings(reasoning_effort=effort),
        )
        
        result = await agent.run(f"Solve this problem:\n{problem}")
        
        print(f"Reasoning Effort: {effort}")
        print(f"Answer: {result.output.answer}")
        print(f"Reasoning:\n{result.output.reasoning}\n")
        print("-" * 70)
    
    print("\nObservations:")
    print("- low: Faster response, direct solution path")
    print("- medium: Balanced speed and reasoning depth")
    print("- high: Thorough analysis, explicit step verification\n")


async def test_complex_planning():
    """Test reasoning effort on a planning task."""
    print("\nReasoning Effort in Planning Tasks\n")
    print("=" * 70)
    
    problem = """
    Optimize a delivery route visiting 5 cities: A, B, C, D, E.
    Distances (km): A-B:120, A-C:85, A-D:95, A-E:140, B-C:70, B-D:90, 
    B-E:80, C-D:50, C-E:110, D-E:75
    Start and end at city A. Find the shortest route.
    """
    
    print(f"Problem: {problem.strip()}\n")
    
    agent = Agent(
        "openai:gpt-4o",
        output_type=Solution,
        model_settings=ModelSettings(reasoning_effort="high"),
    )
    
    result = await agent.run(f"Solve this traveling salesman problem:\n{problem}")
    
    print(f"Answer: {result.output.answer}")
    print(f"Reasoning:\n{result.output.reasoning}\n")
    print("-" * 70)


async def main():
    
    await test_reasoning_effort()
    await test_complex_planning()
    

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
