from loguru import logger as log
from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIChatModel
from pydantic_ai.providers.ollama import OllamaProvider

ollama_model = OpenAIChatModel(
    model_name="bielik",
    provider=OllamaProvider(base_url="http://localhost:11434/v1"),
)
agent = Agent(ollama_model, system_prompt="Jesteś asystentem AI odpowiadającym krótko i zwięźle")


def main(agent: Agent = agent) -> None:
    result = agent.run_sync("Cześć, kim jesteś?")
    log.info(result.output)
    log.info(result.usage())


if __name__ == "__main__":
    main()
