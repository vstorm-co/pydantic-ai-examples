import asyncio
import time

from loguru import logger as log
from shared_fns import main_basic

if __name__ == "__main__":
    # Measure execution time for performance insights
    start_time = time.perf_counter()
    try:
        # Execute the basic OCR pipeline:
        # 1. Loads all PDFs from ./files/samples/
        # 2. Converts each PDF to individual page images (JPG)
        # 3. Sends each image to the LLM via PydanticAI Agent
        # 4. LLM performs OCR and returns unstructured Markdown text
        # 5. Results are saved to JSON files in ./files/results/
        asyncio.run(main_basic())
    except Exception as e:
        log.exception(e)

    end_time = time.perf_counter() - start_time
    log.info(f"Analysis took: {end_time:.1f} seconds")
