import asyncio
import time

from loguru import logger as log
from shared_fns import main_structured

if __name__ == "__main__":
    start_time = time.perf_counter()
    try:
        asyncio.run(main_structured())
    except Exception as e:
        log.exception(e)

    end_time = time.perf_counter() - start_time
    log.info(f"Analysis took: {end_time:.1f} seconds")
