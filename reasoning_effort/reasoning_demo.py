from dotenv import load_dotenv
from pydantic import BaseModel, Field
from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIResponsesModelSettings, ReasoningEffort

load_dotenv()


class Solution(BaseModel):
    answer: str = Field(description="Solution to the problem")


async def test_reasoning_effort():
    """Compare reasoning effort levels on a complex problem."""
    print("Reasoning Effort Parameter Comparison\n")
    print("=" * 70)

    problem = """
    A farmer has chickens and rabbits. There are 35 heads and 94 legs total.
    How many chickens and how many rabbits are there?
    """

    print(f"Problem: {problem.strip()}\n")

    efforts: list[ReasoningEffort] = ["low", "medium", "high"]

    for effort in efforts:
        agent: Agent[None, Solution] = Agent(
            "openai:gpt-5.2",
            output_type=Solution,
            model_settings=OpenAIResponsesModelSettings(
                openai_reasoning_effort=effort,
                openai_reasoning_summary="detailed",
            ),
        )

        result = await agent.run(f"Solve this problem:\n{problem}")

        print(f"Reasoning Effort: {effort}")
        print(f"Answer: {result.output.answer}")
        print("-" * 70)


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

    agent: Agent[None, Solution] = Agent(
        "openai:gpt-5.2",
        output_type=Solution,
        model_settings=OpenAIResponsesModelSettings(
            openai_reasoning_effort="high",
            openai_reasoning_summary="detailed",
        ),
    )

    result = await agent.run(f"Solve this traveling salesman problem:\n{problem}")

    print(f"Answer: {result.output.answer}")
    print("-" * 70)


async def main():
    await test_reasoning_effort()
    await test_complex_planning()


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
