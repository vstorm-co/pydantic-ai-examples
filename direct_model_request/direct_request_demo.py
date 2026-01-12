from dotenv import load_dotenv
from pydantic_ai import ModelRequest
from pydantic_ai.direct import model_request_sync

load_dotenv()


def basic_sync_example():
    """Basic synchronous direct model request."""
    prompt = "What is the capital of France? Answer briefly."
    print("Basic Synchronous Direct Model Request\n")
    response = model_request_sync("openai:gpt-5.2", [ModelRequest.user_text_prompt(prompt)])
    print(f"Request: {prompt}")
    print(f"Response: {response.parts[0].content}")
    print(f"Usage: {response.usage}")
    print()


def main():
    print("PydanticAI Direct Model Request Example\n")
    basic_sync_example()


if __name__ == "__main__":
    main()
