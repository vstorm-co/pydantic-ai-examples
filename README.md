# PydanticAI Examples

A comprehensive collection of examples demonstrating PydanticAI framework capabilities, from basic model requests to advanced document processing with schema validation.

## Prerequisites

### System Requirements

- Python 3.10+
- `uv` package manager

### Environment Setup

```bash
# Install dependencies
uv sync

# Create .env file with your API key
echo "OPENAI_API_KEY=your-key-here" > .env
```

**Note**: Most examples use OpenAI's GPT-4o. Ensure your API key has appropriate permissions and sufficient quota.

## Examples Overview

### 1. Direct Model Requests

**Location**: `direct_model_request/`

Demonstrates direct model API calls without using Agents.

- Basic synchronous model requests using gpt-5.2
- When to use direct API vs Agents
- Simple text prompt handling

[View Example →](direct_model_request/)

### 2. Model Parameters

**Location**: `temperature/`

Control model behavior using temperature.

- Temperature effects on creativity vs consistency
- Practical configuration examples
- Use case recommendations

[View Example →](temperature/)

### 3. Reasoning Effort

**Location**: `reasoning_effort/`

Demonstrates reasoning_effort parameter for gpt-5.2.

- Control depth of internal reasoning
- Complex problem-solving examples
- Trade-off between accuracy and latency

[View Example →](reasoning_effort/)

### 4. Basic Sentiment Classification

**Location**: `basic_sentiment/`

Fixed 3-class sentiment analysis (positive/negative/neutral) with structured outputs.

- Fixed Literal types defined at design time
- Simple accuracy evaluation
- Type-safe results with Pydantic validation

[View Example →](basic_sentiment/)

### 5. Dynamic Classification

**Location**: `dynamic_classification/`

Runtime-adaptable classification that handles any number of classes dynamically.

- Dynamic Literal type generation using `create_model()`
- Same code handles binary, multi-class, and fine-grained classification

[View Example →](dynamic_classification/)

### 6. Bielik Examples with Local Models

**Location**: `bielik_example/`

Learn to use **Bielik**, a Polish language LLM, with PydanticAI running locally via Ollama.

- **Basic Inference**: Simple agent setup and synchronous requests
- **Tool Calling**: Custom tools, multi-turn conversations, async operations
- Local model serving without cloud API dependencies
- Perfect for understanding agent architecture with a real model

[View Example →](bielik_example/)

### 7. Conversation History Management

**Location**: `history_processor/`

Learn how to manage conversation history in AI agents.

- Basic history handling and inspection
- Multi-turn conversations with context awareness
- History persistence (JSON and Database)
- Advanced filtering and transformation
- Context window management strategies (fixed, dynamic, and tool-aware)
- Production-ready database archival

[View Example →](history_processor/)

### 8. OCR Parsing with Data Validation

**Location**: `ocr_parsing/`

Learn how to work with documents using PydanticAI for OCR (Optical Character Recognition).

- **Basic OCR**: Unstructured text extraction from PDFs
- **Structured Output**: Type-safe document analysis with schema validation
- **Validation Errors**: Error handling when LLM output doesn't match schema
- PDF to image conversion pipeline
- Parallel async processing with concurrency control
- Production-ready document processing patterns

[View Example →](ocr_parsing/)

## Quick Start

### Setup

```bash
# Install dependencies
uv sync

# Set API key
echo "OPENAI_API_KEY=your-key" > .env
```

### Run Examples

```bash
# Direct model requests
cd direct_model_request
uv run direct_request_demo.py

# Model parameters
cd temperature
uv run temperature_demo.py

# Reasoning effort
cd reasoning_effort
uv run reasoning_demo.py

# Basic sentiment classifier
cd basic_sentiment
uv run sentiment_classifier.py

# Dynamic classifier
cd dynamic_classification
uv run dynamic_classifier.py

# Bielik local model examples
# Note: Requires Ollama setup (see bielik_example/README.md)
cd bielik_example
uv run bielik_basic_inference.py
uv run bielik_basic_tools.py

# History processor - Run individual examples
cd history_processor
uv run 1_basic_history_handling.py
uv run 2_continuous_history.py
uv run 3_history_usage.py
uv run 4_history_filtering.py
uv run 5a_history_length_fixed.py
uv run 5b_history_length_dynamic.py
uv run 5c_history_with_tools.py
uv run 6_persistent_history.py

# OCR Parsing - Run examples in order
cd ocr_parsing
uv run 1_basic_ocr_demo.py
uv run 2_ocr_with_structured_output.py
uv run 3_ocr_validation.py  # Uncomment validation line in code first
```

## Key Concepts Demonstrated

### Agents

Most examples use PydanticAI's `Agent` class, which wraps an LLM with:

- System prompts to guide behavior
- Output type schemas for structured responses
- Async/await support for concurrent requests

### Structured Outputs

Examples show how to enforce type safety using Pydantic `BaseModel`:

- Basic classification: `Literal` types
- Dynamic classification: `create_model()` for runtime schemas
- OCR parsing: Complex nested schemas with validation

### Async Concurrency

Several examples demonstrate async patterns:

- Parallel processing with `asyncio.gather()`
- Semaphore-based rate limiting
- Efficient handling of multiple documents

### Context & History

Learn how to manage conversational context:

- Persistent history storage
- Token-aware context windowing
- History filtering and transformation

### Local Models

Bielik example shows alternative to cloud APIs:

- Local model serving with Ollama
- Custom tool integration
- Same agent patterns as OpenAI models

## Project Structure

```bash
├── direct_model_request/
│   ├── direct_request_demo.py
│   └── README.md
├── temperature/
│   ├── temperature_demo.py
│   └── README.md
├── reasoning_effort/
│   ├── reasoning_demo.py
│   └── README.md
├── basic_sentiment/
│   ├── sentiment_classifier.py
│   └── README.md
├── dynamic_classification/
│   ├── dynamic_classifier.py
│   └── README.md
├── bielik_example/
│   ├── bielik_basic_inference.py
│   ├── bielik_basic_tools.py
│   ├── Modelfile
│   ├── README.md
│   └── (optional) .env
├── history_processor/
│   ├── 1_basic_history_handling.py
│   ├── 2_continuous_history.py
│   ├── 3_history_usage.py
│   ├── 4_history_filtering.py
│   ├── 5a_history_length_fixed.py
│   ├── 5b_history_length_dynamic.py
│   ├── 5c_history_with_tools.py
│   ├── 6_persistent_history.py
│   ├── README.md
│   ├── output_3.json
├── ocr_parsing/
│   ├── 1_basic_ocr_demo.py
│   ├── 2_ocr_with_structured_output.py
│   ├── 3_ocr_validation.py
│   ├── shared_fns.py
│   ├── README.md
│   ├── files/
│   │   ├── samples/        # Sample PDF documents
│   │   ├── temp_files/      # Temporary image files during processing
│   │   ├── results/        # Output JSON files
├── pyproject.toml
└── README.md
```

## Learning Path

**Recommended order for learning PydanticAI**:

1. **[Direct Model Requests](direct_model_request/)** - Understand basic LLM API calls
2. **[Basic Sentiment](basic_sentiment/)** - Learn structured outputs with Pydantic
3. **[Temperature](temperature/)** - Understand model parameters
4. **[Dynamic Classification](dynamic_classification/)** - Runtime schema generation
5. **[Bielik](bielik_example/)** - Local models and tools
6. **[History Processor](history_processor/)** - Multi-turn conversations
7. **[OCR Parsing](ocr_parsing_demo/)** - Complex real-world document processing

## Common Issues & Troubleshooting

### API Key Issues

- Ensure `OPENAI_API_KEY` is set in `.env`
- Verify key has appropriate permissions
- Check for rate limiting (503 errors)

### Import Errors

- Run `uv sync` to install all dependencies
- Verify you're using Python 3.10+

### Async Issues

- Some examples require async-compatible event loops
- On Windows, you may need to set event loop policy

### OCR-Specific Issues

- **poppler not found**: Install via your package manager (brew/apt/choco)
- **PDF conversion fails**: Ensure PDF is valid and readable
- **Rate limiting**: Reduce semaphore value in `shared_fns.py`

See individual example READMEs for specific setup requirements.

## Resources

- [Python Documentation](https://docs.python.org/3/)
- [PydanticAI Documentation](https://ai.pydantic.dev/)
- [Pydantic Documentation](https://docs.pydantic.dev/)
- [OpenAI API Reference](https://platform.openai.com/docs/api-reference)
- [Python asyncio Guide](https://docs.python.org/3/library/asyncio.html)

## Contributing

Found an issue or have an improvement? Feel free to contribute to this example repository.
