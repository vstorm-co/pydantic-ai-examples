"""
Bielik Tool Calling Example

This script demonstrates how to equip a PydanticAI Agent with custom tools,
enabling it to perform external actions beyond pure language generation.

Key concepts:
1. Tool Definition: Functions decorated with @agent.tool become available to the model
2. Tool Calling: The model can request to use a tool when it determines it's needed
3. Tool Context: RunContext provides access to agent state during tool execution
4. Message History: Maintaining conversation history allows multi-turn interactions
5. Async Operations: Tools can perform asynchronous operations like HTTP requests

In this example, we implement two tools:
- roll_dice: Simulates rolling a 6-sided dice
- check_weather: Fetches real weather data from WeatherAPI

This demonstrates how modern LLMs can be enhanced with real-world capabilities
by integrating them with external APIs and services.
"""

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

# Load environment variables from .env file
# WEATHER_API_KEY should be set here for the weather tool to work
load_dotenv(override=True)


# API Configuration
# =================
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")
if not WEATHER_API_KEY:
    raise RuntimeError(
        "WEATHER_API_KEY environment variable is not set. Please define it (e.g., in your .env file) so the weather tool can work."
    )

# Ollama Model Configuration
# ===========================
# The Bielik model needs to be properly configured for tool calling:
# - Use a version that supports tool calling (e.g., bielik_v3_q8_tools)
# - The Modelfile in this directory specifies the tool calling format
# - Temperature is set to 0.1 for more deterministic outputs during tool calling
ollama_model = OpenAIChatModel(
    model_name="bielik_v3_q8_tools",
    provider=OllamaProvider(base_url="http://localhost:11434/v1"),
)

# Create the Agent with tools
# ============================
# The @agent.tool decorator registers functions as tools available to the model.
# The agent will analyze when to call these tools based on user requests.
agent = Agent(ollama_model, system_prompt="Jesteś pomocnym asystentem AI")


@agent.tool
async def roll_dice(ctx: RunContext[None]) -> int:
    """
    Tool: Roll a virtual dice

    Simulates rolling a standard 6-sided dice and returns a random number between 1 and 6.
    This is a simple tool that doesn't require external API calls.

    Args:
        ctx: RunContext providing access to the agent's state (not used in this simple case)

    Returns:
        int: A random integer between 1 and 6 (inclusive)
    """
    # Use secrets for cryptographically secure random selection
    output = secrets.choice([1, 2, 3, 4, 5, 6])

    # Debug logging to show when the tool is called and what it returns
    ic(f"[TOOL CALL] Output from tool '{roll_dice.__name__}'")
    ic(output)
    return output


@agent.tool
async def check_weather(ctx: RunContext[None], city: str) -> Any:
    """
    Tool: Check current weather conditions

    Fetches real-time weather data for a specified city using the WeatherAPI service.
    This demonstrates how to integrate external APIs as agent tools.

    Prerequisites:
    - WEATHER_API_KEY environment variable must be set
    - API key can be obtained for free from https://www.weatherapi.com/
    - The API is called asynchronously to avoid blocking

    Args:
        ctx: RunContext providing access to the agent's state (not used here)
        city (str): The name of the city to check weather for

    Returns:
        dict: A simplified weather data object containing:
            - location: City name
            - temp_c: Temperature in Celsius
            - condition: Weather condition description (e.g., "Sunny", "Rainy")
        OR
        str: An error message if the API call fails
    """
    # WeatherAPI endpoint for current weather
    url = "https://api.weatherapi.com/v1/current.json"

    # Query parameters for the API request
    params = {
        "key": WEATHER_API_KEY,  # Authentication key
        "q": city,  # City name to query
        "aqi": "no",  # Disable air quality data for simpler response
    }

    # Make asynchronous HTTP request using httpx client
    async with httpx.AsyncClient() as client:
        response = await client.get(url, params=params)

        if response.status_code == 200:
            # Successfully retrieved weather data
            data = response.json()

            # Extract relevant fields from the API response
            # This simplification makes the data more digestible for the LLM
            output = {
                "location": data["location"]["name"],
                "temp_c": data["current"]["temp_c"],
                "condition": data["current"]["condition"]["text"],
            }

            # Debug logging
            ic(f"[TOOL CALL] Output from tool '{check_weather.__name__}'")
            ic(output)
            return output
        else:
            # Handle API errors gracefully
            return f"Error: Could not find weather for {city}. Status: {response.status_code}"


async def main(agent: Agent = agent) -> None:
    """
    Main function demonstrating multi-turn conversation with tool calling.

    This function shows how to:
    1. Make the first request to establish context
    2. Pass message history to maintain conversation context
    3. Have the agent use tools when appropriate
    4. Access and log the agent's reasoning and tool calls

    The three prompts demonstrate:
    - Prompt 1: Basic greeting (no tool needed)
    - Prompt 2: Requesting tool use (roll_dice)
    - Prompt 3: Requesting tool use with parameters (check_weather)
    """

    # First turn: Greeting
    # ====================
    # This initial message establishes context and allows the model to introduce itself
    prompt_1 = "Cześć, kim jesteś?"  # "Hello, who are you?" in Polish
    result_1 = await agent.run(prompt_1)
    log.info(prompt_1)
    log.info(f"Response: {result_1.output}")

    # Second turn: Tool calling - roll_dice
    # ======================================
    # Pass the message history from the previous turn to maintain context
    # The agent will understand it's continuing a conversation and can use tools
    prompt_2 = "Rzuć kostką i podaj wynik!"  # "Roll a dice and tell me the result!" in Polish
    result_2 = await agent.run(prompt_2, message_history=result_1.all_messages())
    log.info(prompt_2)
    log.info(f"Response: {result_2.output}")

    # Optional: Inspect all messages including tool calls
    # This shows the full conversation including tool call requests and responses
    # Uncomment to see the detailed message structure:
    # ic(result_2.all_messages())

    # Third turn: Tool calling - check_weather
    # =========================================
    # Continue the conversation with another tool-requiring request
    prompt_3 = "Sprawdź pogodę w Warszawie, proszę Cię!"  # "Check the weather in Warsaw, please!" in Polish
    result_3 = await agent.run(prompt_3, message_history=result_2.all_messages())
    log.info(prompt_3)
    log.info(f"Response: {result_3.output}")

    # Optional: Inspect the full message history
    # This includes the agent's tool call request and the tool result
    # Uncomment to see exactly what the agent sent and received:
    # ic(result_3.all_messages())


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
