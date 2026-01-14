import asyncio
import time

from loguru import logger as log
from shared_fns import main_structured

if __name__ == "__main__":
    # Measure execution time for performance insights
    start_time = time.perf_counter()
    try:
        # Execute the structured OCR pipeline:
        # 1. Loads all PDFs from ./files/samples/
        # 2. Converts each PDF to individual page images (JPG)
        # 3. Sends each image to the LLM via PydanticAI Agent (with output_type schema)
        # 4. LLM analyzes the document and returns STRUCTURED JSON with:
        #    - file_type: Document classification (invoice, instruction, etc.)
        #    - file_content_md: OCR output as Markdown
        #    - file_elements: List of detected elements (tables, paragraphs, images)
        # 5. Pydantic validates all responses match the schema (strict type checking)
        # 6. Results are saved to JSON files with 'structured_' prefix
        asyncio.run(main_structured())
    except Exception as e:
        log.exception(e)

    end_time = time.perf_counter() - start_time
    log.info(f"Analysis took: {end_time:.1f} seconds")
