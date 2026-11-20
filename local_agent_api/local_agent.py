"""Call a locally published sample agent through PydanticAI's OpenAI adapter."""

import argparse
import asyncio
from pathlib import Path

import httpx2
from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIChatModel
from pydantic_ai.providers.openai import OpenAIProvider


async def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--port", type=int, default=8787)
    parser.add_argument("--key-file", type=Path, required=True)
    parser.add_argument("--stream", action="store_true")
    args = parser.parse_args()

    # Do not route the local request through environment-configured proxies.
    async with httpx2.AsyncClient(trust_env=False, timeout=15) as client:
        provider = OpenAIProvider(
            base_url=f"http://127.0.0.1:{args.port}/v1",
            api_key=args.key_file.read_text(encoding="utf-8").strip(),
            http_client=client,
        )
        agent = Agent(OpenAIChatModel("agent/sample", provider=provider))
        prompt = "Show the offline sample response."
        if args.stream:
            async with agent.run_stream(prompt) as result:
                async for delta in result.stream_text(delta=True, debounce_by=None):
                    print(delta, end="", flush=True)
            print()
        else:
            print((await agent.run(prompt)).output)


if __name__ == "__main__":
    asyncio.run(main())
