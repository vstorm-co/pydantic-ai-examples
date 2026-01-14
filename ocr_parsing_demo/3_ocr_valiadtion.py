from loguru import logger as log
from pydantic import BaseModel, ValidationError


# 1. This is your schema from the original code
# It expects file_elements to be a LIST of FileElement objects
class FileElement(BaseModel):
    element_type: str
    element_content: str


class ModelAnalysisOutput(BaseModel):
    file_type: str
    file_content_md: str
    file_elements: list[FileElement]  # <--- MUST BE A LIST


# 2. Simulated "Bad Data" from an LLM
# Here, the LLM sent a string "No elements found" instead of an empty list []
bad_llm_data = {
    "file_type": "invoice",
    "file_content_md": "# Invoice Content",
    "file_elements": ["No elements found"],  # This will trigger the error
}


# 3. Explicit Validation Catch
def demonstrate_validation_error():
    try:
        log.info("Attempting to validate LLM response...")
        # This is what happens under the hood in agent_structured.run()

        ### REMARK ###
        # Line below has to be uncommented to trigger the `ValidationError`
        # we're looking and waiting for
        # _ = ModelAnalysisOutput(**bad_llm_data)

    except ValidationError as e:
        log.error("--- VALIDATION ERROR DETECTED ---")

        # We iterate through the errors to show exactly what went wrong
        for error in e.errors():
            field = error["loc"][0]
            error_type = error["type"]
            message = error["msg"]
            input_received = error["input"]

            log.info(f"❌ Field: '{field}'")
            log.info(f"Error Type: {error_type}")
            log.info(f"Reason: {message}")
            log.info(f'What the LLM actually sent: "{input_received}"')
            log.info("Expected: A list of objects, not a string.")


if __name__ == "__main__":
    demonstrate_validation_error()
