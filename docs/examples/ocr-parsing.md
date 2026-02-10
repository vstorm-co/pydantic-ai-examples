---
title: OCR Parsing
---

# OCR Parsing with PydanticAI

These examples demonstrate document processing capabilities using PydanticAI for OCR (Optical Character Recognition). From basic text extraction to structured output with schema validation.

## Setup

!!! note "macOS Users"
    Install the `poppler` dependency required by `pdf2image`:

    ```bash
    brew install poppler
    ```

    For other platforms, see [Troubleshooting](#troubleshooting) below.

## Examples

### 1. Basic OCR Demo

**File:** `1_basic_ocr_demo.py`

Demonstrates a basic flow for OCR on various document types. Output is Markdown-formatted content — LLMs excel at Markdown formatting tasks.

??? example "Sample Output"
    ```markdown
    # Invoice

    YesLogic Pty. Ltd.
    7 / 39 Bouverie St
    Carlton VIC 3053
    Australia

    **Invoice date:** Nov 26, 2016
    **Invoice number:** 161126
    **Payment due:** 30 days after invoice date

    | Description               | From         | Until        | Amount      |
    |---------------------------|-------------|-------------|-------------|
    | Prince Upgrades & Support | Nov 26, 2016 | Nov 26, 2017 | USD $950.00 |
    | **Total**                 |             |             | USD $950.00 |
    ```

### 2. OCR with Structured Output

**File:** `2_ocr_with_structured_output.py`

Uses Pydantic `BaseModel` schemas provided to the LLM **before** inference starts. Combined with a customized prompt, the results are high quality with built-in type verification.

Output structure:

```json
{
    "filename": "file_name_page_1.jpg",
    "analysis_result": {
        "file_type": "invoice",
        "file_content_md": "# Sunny Farm ...",
        "file_elements": [
            {
                "element_type": "table",
                "element_content": "| Item | Price | ... |"
            }
        ]
    }
}
```

!!! tip "Why Structured Output?"
    The upside of this approach is built-in verification of returned data types — ensuring you get the structure you want on every inference.

### 3. OCR Validation

**File:** `3_ocr_validation.py`

Demonstrates purposeful `ValidationError` handling when LLM output doesn't match the expected schema. Uses a simplified Pydantic model to highlight validation behavior.

```
| ERROR | demonstrate_validation_error:35 - --- VALIDATION ERROR DETECTED ---
| INFO  | demonstrate_validation_error:44 - Field: 'file_elements'
| INFO  | demonstrate_validation_error:45 - Error Type: model_type
| INFO  | demonstrate_validation_error:46 - Reason: Input should be a valid dictionary
                                           or instance of FileElement
| INFO  | demonstrate_validation_error:47 - What the LLM actually sent: "No elements found"
```

## Running

```bash
cd ocr_parsing

# Basic OCR
uv run 1_basic_ocr_demo.py

# Structured output
uv run 2_ocr_with_structured_output.py

# Validation errors (uncomment validation line in code first)
uv run 3_ocr_validation.py
```

## Key Concepts

- **PDF to image conversion** — Each PDF page is converted to `.jpg` for optimal LLM input
- **Structured schemas** — Pydantic models enforce output structure and type safety
- **Parallel async processing** — Semaphore-based concurrency control for multiple documents
- **Validation errors** — Graceful handling when LLM output doesn't match the schema

## Troubleshooting

!!! warning "poppler not found"
    === "macOS"
        ```bash
        brew install poppler
        ```
    === "Linux (Ubuntu/Debian)"
        ```bash
        sudo apt-get install poppler-utils
        ```
    === "Windows"
        ```bash
        choco install poppler
        ```
        Or download from [Poppler releases](https://github.com/oschwartz10612/poppler-windows/releases/) and add to PATH.

!!! warning "Rate limiting or timeout errors"
    Concurrency is limited to 5 parallel requests via semaphore. If you still hit rate limits, reduce the value in `shared_fns.py`:

    ```python
    semaphore = asyncio.Semaphore(3)  # Reduce from 5 to 3
    ```

## File Samples

All sample files were downloaded from [Prince XML](https://www.princexml.com/samples/).
