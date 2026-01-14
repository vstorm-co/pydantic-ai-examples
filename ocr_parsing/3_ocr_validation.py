from loguru import logger as log
from pydantic import BaseModel, ValidationError

# ==============================================================================
# STEP 1: Define the expected schema
# ==============================================================================
# When using structured output with PydanticAI, you define a Pydantic BaseModel
# that tells the LLM exactly what structure you expect back.


class FileElement(BaseModel):
    element_type: str
    element_content: str


class ModelAnalysisOutput(BaseModel):
    file_type: str
    file_content_md: str
    file_elements: list[FileElement]  # <--- MUST BE A LIST of FileElement objects


# ==============================================================================
# STEP 2: Example of bad LLM output
# ==============================================================================
# Sometimes LLMs don't follow the schema perfectly. Here's what happens if
# the LLM sends a string instead of a list for file_elements.
# Pydantic will automatically detect and reject this invalid data.

bad_llm_data = {
    "file_type": "invoice",
    "file_content_md": "# Invoice Content",
    "file_elements": ["No elements found"],  # ❌ WRONG: String instead of FileElement object
}


# ==============================================================================
# STEP 3: Demonstration of validation error handling
# ==============================================================================
# This function shows how Pydantic catches and reports schema violations.
# This is a key safety feature of structured output - you get validation
# errors instead of corrupted data making it into your application.


def demonstrate_validation_error():
    try:
        log.info("Attempting to validate LLM response...")
        # This is what happens under the hood when agent_structured.run() receives data

        ### REMARK ###
        # Line below has to be uncommented to trigger the `ValidationError`
        # we're looking and waiting for. This shows how Pydantic validates
        # the LLM's response against your schema.
        # _ = ModelAnalysisOutput(**bad_llm_data) # <-- uncomment this line
        ### REMARK ###

    except ValidationError as e:
        log.error("--- VALIDATION ERROR DETECTED ---")
        log.info("Pydantic rejected the LLM output because it doesn't match the schema.")

        # Iterate through all validation errors to understand what went wrong
        for error in e.errors():
            field = error["loc"][0]  # Which field caused the error?
            error_type = error["type"]  # Type of validation failure
            message = error["msg"]  # Detailed error message
            input_received = error["input"]  # What data was actually received

            log.info(f"❌ Field: '{field}'")
            log.info(f"Error Type: {error_type}")
            log.info(f"Reason: {message}")
            log.info(f'What the LLM actually sent: "{input_received}"')
            log.info("Expected: A list of objects, not a string.")


if __name__ == "__main__":
    demonstrate_validation_error()
