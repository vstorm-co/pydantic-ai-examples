# Direct Model Request Demo

This example demonstrates how to use pydantic-ai's **direct API** to make model requests without creating an Agent. The direct API is ideal when you need more control over model interactions or want to implement custom behavior.

## When to Use Direct API vs Agent

**Use Direct API when:**
- You need more direct control over model interactions
- You want to implement custom behavior around model requests  
- You're building your own abstractions on top of model interactions

**Use Agent API for:**
- Most application use cases (provides higher-level convenience)
- Built-in tool execution, retrying, structured output parsing
- More complex multi-turn conversations

## Example Included

### Basic Synchronous Request
Simple direct model call using `model_request_sync()` with OpenAI's gpt-5.2 model


## Running

```bash

cd direct_model_request
uv run direct_request_demo.py
```

## Key Features Demonstrated

- **Direct model requests** without Agent abstraction
- **Synchronous** request patterns
- **Simple text prompts** and response handling

## Learn More

- [Pydantic AI Direct API Documentation](https://ai.pydantic.dev/direct/)
- [Agent vs Direct API Comparison](https://ai.pydantic.dev/direct/#when-to-use-the-direct-api-vs-agent)
