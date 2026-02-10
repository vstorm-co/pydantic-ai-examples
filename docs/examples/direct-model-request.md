---
title: Direct Model Requests
---

# Direct Model Requests

This example demonstrates how to use PydanticAI's **direct API** to make model requests without creating an Agent. The direct API is ideal when you need more control over model interactions or want to implement custom behavior.

## When to Use Direct API vs Agent

| Direct API | Agent API |
|---|---|
| More direct control over model interactions | Most application use cases |
| Custom behavior around model requests | Built-in tool execution, retrying, structured output |
| Building your own abstractions | Complex multi-turn conversations |

## Running

```bash
cd direct_model_request
uv run direct_request_demo.py
```

## Code Comparison: Direct API vs Agent

Here's a side-by-side look at how you'd accomplish the same task using both approaches:

=== "Direct API"

    ```python
    from pydantic_ai import ModelRequest
    from pydantic_ai.direct import model_request_sync

    prompt = "What is the capital of France? Answer briefly."

    response = model_request_sync(
        "openai:gpt-5.2",
        [ModelRequest.user_text_prompt(prompt)],
    )

    print(response.parts[0].content)
    ```

=== "Agent"

    ```python
    from pydantic_ai import Agent

    agent = Agent("openai:gpt-5.2")

    result = agent.run_sync("What is the capital of France? Answer briefly.")

    print(result.output)
    ```

The **Direct API** gives you raw access to the model request/response cycle — you construct `ModelRequest` objects yourself and work with response parts directly. The **Agent** wraps this in a higher-level interface that handles tool execution, retries, and structured output for you.

!!! info "When to Choose Direct API"
    The direct API gives you lower-level access when you need it. For most applications, the Agent API is the better choice — it handles retries, tool execution, and structured output parsing automatically.

## Learn More

- [PydanticAI Direct API Documentation](https://ai.pydantic.dev/direct/)
- [Agent vs Direct API Comparison](https://ai.pydantic.dev/direct/#when-to-use-the-direct-api-vs-agent)
