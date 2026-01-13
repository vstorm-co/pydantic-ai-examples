import os
import secrets
from typing import Any

import httpx
from dotenv import load_dotenv
from icecream import ic
from loguru import logger as log
from pydantic_ai import Agent, RunContext
from pydantic_ai.models.openai import OpenAIChatModel
from pydantic_ai.providers.ollama import OllamaProvider

load_dotenv(override=True)


WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")

# Ollama model setup
ollama_model = OpenAIChatModel(
    model_name="bielik_v3_q8_tools",
    provider=OllamaProvider(base_url="http://localhost:11434/v1"),
)

# Agent with tools setup
agent = Agent(ollama_model, system_prompt="Jesteś pomocnym asystentem AI")


@agent.tool
async def roll_dice(ctx: RunContext[None]) -> int:
    "Rolls a dice to get a number from 1 to 6"
    output = secrets.choice([1, 2, 3, 4, 5, 6])
    ic(f"[TOOL CALL] Output from tool '{roll_dice.__name__}'")
    ic(output)
    return output


@agent.tool
async def check_weather(ctx: RunContext[None], city: str) -> Any:
    """
    Tool used to check the weather in the given city.

    Args:
        city (str): Name of the city where weather should be checked

    Returns:
        weather_data (Any)
    """
    url = "http://api.weatherapi.com/v1/current.json"
    params = {"key": WEATHER_API_KEY, "q": city, "aqi": "no"}

    async with httpx.AsyncClient() as client:
        response = await client.get(url, params=params)
        if response.status_code == 200:
            data = response.json()

            # simplified return
            output = {
                "location": data["location"]["name"],
                "temp_c": data["current"]["temp_c"],
                "condition": data["current"]["condition"]["text"],
            }

            ic(f"[TOOL CALL] Output from tool '{check_weather.__name__}'")
            ic(output)
            return output
        else:
            return f"Error: Could not find weather for {city}. Status: {response.status_code}"


def main(agent: Agent = agent) -> None:
    prompt_1 = "Cześć, kim jesteś?"
    result_1 = agent.run_sync(prompt_1)
    log.info(prompt_1)
    log.info(result_1.output)
    # ic(result_1.all_messages())

    prompt_2 = "Rzuć kostką i podaj wynik!"
    result_2 = agent.run_sync(prompt_2, message_history=result_1.all_messages())
    log.info(prompt_2)
    log.info(result_2.output)

    # Optional: closer look on how does tool calling look under the hood
    # ic(result_2.all_messages())

    prompt_3 = "Sprawdź pogodę w Warszawie, proszę Cię!"
    result_3 = agent.run_sync(prompt_3, message_history=result_2.all_messages())
    log.info(prompt_3)
    log.info(result_3.output)

    # Optional: closer look on how does tool calling look under the hood
    # ic(result_3.all_messages())


if __name__ == "__main__":
    main()
