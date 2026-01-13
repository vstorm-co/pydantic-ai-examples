"""
Bielik Basic Inference Example

This script demonstrates the simplest way to use the Bielik LLM model with PydanticAI.
It shows how to:
1. Set up a local Ollama model connection
2. Create a PydanticAI Agent with a system prompt
3. Run a synchronous inference (request-response interaction)
4. Access the model's output and usage statistics

The Bielik model is a Polish language LLM based on Llama, which makes it excellent
for Polish language understanding and generation tasks.
"""

from loguru import logger as log
from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIChatModel
from pydantic_ai.providers.ollama import OllamaProvider

# Configuration of the Bielik model through Ollama
# ================================================
# - model_name: The identifier of the model as registered in Ollama
# - provider: OllamaProvider connects to a locally running Ollama instance
# - base_url: The endpoint where Ollama is serving the model (default: localhost:11434)
#   This assumes you've already started Ollama and pulled the bielik model locally
ollama_model = OpenAIChatModel(
    model_name="bielik_v3_q8_tools",
    provider=OllamaProvider(base_url="http://localhost:11434/v1"),
)

# Create a PydanticAI Agent
# =========================
# An Agent is the main interface for interacting with the LLM. It:
# - Wraps the language model
# - Manages conversation context and message history
# - Can be equipped with tools (see bielik_basic_tools.py for advanced usage)
# - system_prompt: Instructions that guide the model's behavior and tone
#   (In this case: "Respond concisely and briefly" in Polish)
agent = Agent(ollama_model, system_prompt="Jesteś asystentem AI odpowiadającym krótko i zwięźle")


def main(agent: Agent = agent) -> None:
    """
    Main function that demonstrates basic inference.

    This function:
    1. Sends a simple greeting to the agent
    2. Receives the model's response
    3. Logs both the output and token usage statistics

    Args:
        agent: The PydanticAI Agent instance to use for inference
    """

    # Run a synchronous request to the agent
    # run_sync() blocks until the model completes its response
    # Unlike run() which is asynchronous, this is simpler for basic use cases
    result = agent.run_sync("Cześć, kim jesteś?")  # "Hello, who are you?" in Polish

    # Log the model's response
    log.info(f"Agent response: {result.output}")

    # Log token usage statistics
    # This shows how many tokens were used for input and output
    # Useful for understanding model costs and efficiency
    log.info(f"Token usage: {result.usage()}")


if __name__ == "__main__":
    main()
