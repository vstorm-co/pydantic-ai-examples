---
title: Local Agent API
---

# Call a local agent with an OpenAI-compatible provider

`OpenAIProvider` can point at a custom endpoint instead of OpenAI. This example
uses a local [Open Agent API](https://github.com/jiangxingfan1-coder/Open-Agent-API)
gateway and its built-in `agent/sample`. The SDK's `model` argument is an agent
ID here, not the name of a foundation model.

## Run the sample

Follow the [source quickstart](https://github.com/jiangxingfan1-coder/Open-Agent-API#running-in-three-minutes).
It starts a loopback server on port 8787 and creates `.oaa/keys/quickstart.key`
in the source checkout by default. This is a local caller key, not an OpenAI key.

From the PydanticAI examples checkout, run:

```bash
uv run --no-project --python 3.13 --with 'pydantic-ai-slim[openai]==2.71.0' \
  local_agent_api/local_agent.py --key-file /path/to/Open-Agent-API/.oaa/keys/quickstart.key
```

Add `--stream` to print deltas as they arrive. If quickstart used a different
port, pass it with `--port`. Both modes print the offline sample response; the
sample includes the current local time, so successive outputs can differ.

The script uses `OpenAIChatModel` with a fixed loopback host and does not read
`OPENAI_API_KEY`. It does not test a real model or an approval flow. Keep the
caller key separate from the gateway's admin token. Stop the gateway from its
source checkout with `npm run oaa -- stop` when done.
