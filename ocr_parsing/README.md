# OCR parsing demo with usage of PydanticAI

These examples provide an overview of possibilities that are open to all of the users of PydanticAI framework.

Since main objective is an OCR process, all sample files for runs are PDFs, some of which have more than one page. Every page is being transferred to a `.jpg` picture, since it is the optimal way to provide data to Agents / LLM without any additional hassle while providing high quality output data.

## Setup

### MacOS users

As a MacOS user you'll need to install additional package used by `pdf2image` package our code is using. You can do so via Brew:

```bash
# Package used by `pdf2image`
brew install poppler
```

## Quick start

```bash
# Move into examples directory
cd ocr_parsing_demo

# Run the scripts
uv run 1_basic_ocr_demo.py
uv run 2_ocr_with_structured_output.py

# Before running 3rd example please investigate the code and uncomment necessary line
uv run 3_ocr_validation.py
```

### `1_basic_ocr_demo.py`

This script demonstrates a basic flow that can be used for OCR purposes on various types of documents. The output is provided as a Markdown formatted content due to LLMs being especially great with Markdown formatting tasks.

A sample of the output can be found below:

```markdown
# Invoice

YesLogic Pty. Ltd.
7 / 39 Bouverie St
Carlton VIC 3053
Australia

[www.yeslogic.com](http://www.yeslogic.com)
ABN 32 101 193 560

---

Customer Name
Street
Postcode City
Country

**Invoice date:** Nov 26, 2016
**Invoice number:** 161126
**Payment due:** 30 days after invoice date

| Description                 | From       | Until      | Amount     |
|-----------------------------|------------|------------|------------|
| Prince Upgrades & Support   | Nov 26, 2016 | Nov 26, 2017 | USD $950.00 |
| **Total**                   |            |            | USD $950.00 |

---

Please transfer amount to:

**Bank account name:** Yes Logic Pty Ltd
**Name of Bank:** Commonwealth Bank of Australia (CBA)
**Bank State Branch (BSB):** 063010
**Bank State Branch (BSB):** 063010
**Bank State Branch (BSB):** 063019
**Bank account number:** 13201652
**Bank SWIFT code:** CTBAAU2S
**Bank address:** 231 Swanston St, Melbourne, VIC 3000, Australia

*The BSB number identifies a branch of a financial institution in Australia. When transferring money to Australia, the BSB number is used together with the bank account number and the SWIFT code. Australian banks do not use IBAN numbers.*

---

[www.yeslogic.com](http://www.yeslogic.com)
```

### `2_ocr_with_structured_output.py`

Second example focuses on the usage of Pydantic's `BaseModel` objects, which are provided to the LLM / Agent BEFORE the inference starts. Along with a customized prompt the results can be very sound and of high quality. The upside of this approach is built-in verification of returned types of the data ensuring we'll be able to get the structure we want on every inference performed.

In this particular example, the output is structured as follows:

```json
{
    "filename": "file_name_page_1.jpg",
    "analysis_result": {
        "file_type": "string type data - file type assessed by the LLM (we can use closed list here)",
        "file_content_md": "string type data - an OCR output formatted as a Markdown text",
        "file_elements": {
            "element_type": "string type data - type of the element found on the page",
            "element_content": "string type data - content of the element found",
            ...
        }
    },
    {...},
    {...}
}
```

Sample output from LLM based on one of the files in the `./files/samples` directory is as follows:

```json
[
    {
        "filename": "invoice_sample_2_page_0",
        "analysis_result": {
            "file_type": "invoice",
            "file_content_md": "# Sunny Farm\n\n**AUSTRALIA FRESH PRODUCE**\n\n**VICTORIA**\n\n123 Somewhere St, Melbourne VIC 3000  \n(03) 1234 5678\n\n---\n\n## ATTENTION TO\n\n**Denny Gunawan**  \n221 Queen St  \nMelbourne VIC 3000\n\n---\n\n## Invoice Number: #20130304\n\n| Organic Items | Price/kg | Quantity(kg) | Subtotal |\n|---------------|----------|--------------|----------|\n| Apple         | $5.00    | 1            | $5.00    |\n| Orange        | $1.99    | 2            | $3.98    |\n| Watermelon    | $1.69    | 3            | $5.07    |\n| Mango         | $9.56    | 2            | $19.12   |\n| Peach         | $2.99    | 1            | $2.99    |\n\n---\n\n## Subtotal: $36.00\n## GST (10%): $3.60\n## Total: **$39.60**\n\n---\n\n**THANK YOU**\n\n*Lorem ipsum dolor sit amet, consectetur adipiscing elit. Aliquam sodales dapibus fermentum. Nunc adipiscing, magna sed scelerisque cursus, erat lectus dapibus urna, sed facilisis leo dui et ipsum.*",
            "file_elements": [
                {
                    "element_type": "image_description",
                    "element_content": "Logo with text 'AUSTRALIA FRESH PRODUCE', 'SUNNY FARM', 'VICTORIA'."
                },
                {
                    "element_type": "paragraph",
                    "element_content": "123 Somewhere St, Melbourne VIC 3000 (03) 1234 5678"
                },
                {
                    "element_type": "paragraph",
                    "element_content": "ATTENTION TO Denny Gunawan 221 Queen St Melbourne VIC 3000"
                },
                {
                    "element_type": "paragraph",
                    "element_content": "Invoice Number: #20130304"
                },
                {
                    "element_type": "table",
                    "element_content": "| Organic Items | Price/kg | Quantity(kg) | Subtotal |\n|---------------|----------|--------------|----------|\n| Apple         | $5.00    | 1            | $5.00    |\n| Orange        | $1.99    | 2            | $3.98    |\n| Watermelon    | $1.69    | 3            | $5.07    |\n| Mango         | $9.56    | 2            | $19.12   |\n| Peach         | $2.99    | 1            | $2.99    |"
                },
                {
                    "element_type": "paragraph",
                    "element_content": "Subtotal: $36.00 GST (10%): $3.60 Total: $39.60"
                },
                {
                    "element_type": "paragraph",
                    "element_content": "THANK YOU"
                },
                {
                    "element_type": "paragraph",
                    "element_content": "*Lorem ipsum dolor sit amet, consectetur adipiscing elit. Aliquam sodales dapibus fermentum. Nunc adipiscing, magna sed scelerisque cursus, erat lectus dapibus urna, sed facilisis leo dui et ipsum.*"
                }
            ]
        }
    }
]
```

### `3_ocr_validation.py`

Last example focuses on purposeful `ValidationError` that happens if the output data we receive from the Agent / LLM is not in line with format we've asked for. Pydantic model used here is simplified just to highlight this particular behavior.

```bash
| INFO     | __main__:demonstrate_validation_error:30 - Attempting to validate LLM response...
| ERROR    | __main__:demonstrate_validation_error:35 - --- VALIDATION ERROR DETECTED ---
| INFO     | __main__:demonstrate_validation_error:44 - ❌ Field: 'file_elements'
| INFO     | __main__:demonstrate_validation_error:45 - Error Type: model_type
| INFO     | __main__:demonstrate_validation_error:46 - Reason: Input should be a valid dictionary or instance of FileElement
| INFO     | __main__:demonstrate_validation_error:47 - What the LLM actually sent: "No elements found"
| INFO     | __main__:demonstrate_validation_error:48 - Expected: A list of objects, not a string.
```

## File samples

All the files were downloaded from [Prince XML](https://www.princexml.com/samples/)

## Troubleshooting

### Issue: `ModuleNotFoundError: No module named 'pdf2image'`

**Solution:** Ensure all dependencies from the root project README are installed via `uv sync`.

### Issue: `poppler not found` (macOS)

**Solution:** Install poppler using Homebrew:

```bash
brew install poppler
```

### Issue: `poppler not found` (Linux - Ubuntu/Debian)

**Solution:** Install via apt:

```bash
sudo apt-get install poppler-utils
```

### Issue: `poppler not found` (Windows)

**Solution:** Install via Chocolatey:

```bash
choco install poppler
```

Or download from [Poppler releases](https://github.com/oschwartz10612/poppler-windows/releases/) and add to PATH.

### Issue: OpenAI API authentication error

**Solution:** Ensure your `.env` file contains a valid `OPENAI_API_KEY`:

```
OPENAI_API_KEY=sk-...
```

Verify the key has appropriate permissions and hasn't expired.

### Issue: Validation errors in example 3

**Expected behavior** - Example 3 is designed to demonstrate validation errors. Uncomment the line in `demonstrate_validation_error()` to see the error handling in action.

### Issue: PDF conversion produces blank images

**Possible causes:**

- Corrupted PDF file
- PDF is image-based without embedded text (actual scanned document)

**Solution:** Try with different PDF files from the `./files/samples/` directory or verify your PDF is readable.

### Issue: Rate limiting or timeout errors

**Solution:** The concurrency is limited to 5 parallel requests (via semaphore). If you still hit rate limits, reduce the semaphore value in `shared_fns.py`:

```python
semaphore = asyncio.Semaphore(3)  # Reduce from 5 to 3
```
