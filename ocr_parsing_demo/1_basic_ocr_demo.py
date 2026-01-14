import asyncio
import json
import os
import tempfile
import time
from pathlib import Path

from dotenv import load_dotenv
from icecream import ic
from loguru import logger as log
from pdf2image import convert_from_path
from pydantic import BaseModel
from pydantic_ai import Agent, BinaryContent
from pydantic_ai.models.openai import OpenAIChatModel
from pydantic_ai.settings import ModelSettings

load_dotenv()

### Setup asyncio boundaries
semaphore = asyncio.Semaphore(5)


### Structuring the output for saving final results
class Results(BaseModel):
    filename: str = ""
    result: str = ""


### Create and setup PydanticAI agent
# Model's temperature is set to `0` for model to be more analytic
# in its work (less temperature = less creativity)
model = OpenAIChatModel("gpt-4o", settings=ModelSettings(temperature=0))
agent = Agent(
    model=model,
    system_prompt="You are an OCR expert specialized in the data extraction \
        from various types of documents. You are always precise and make sure \
        that extraction is done properly.",
)

prompt = "Provided below you can find a document. "
"Perform a full-scale OCR process on it. Return its content in the Markdown "
"format and try to retain as much of original structure as possible. "
"Use elements like tables, image descriptions, lists, headers and others. "
"Do not perform any additional actions other than recognition of the characters "
"in the document and translating it into a Markdown result."


### Methods
async def list_all_files(directory: Path, extension: str = "pdf") -> list[Path]:
    """List all files in a directory with provided extension

    Args:
        dir (Path): directory to be checked
        extension (str, optional): file extension of files to be listed. Defaults to "pdf".

    Returns:
        list[Path]: a list of filepaths for further analysis
    """
    return [Path(directory, f) for f in os.listdir(directory) if f.lower().endswith(extension)]


async def pdf_to_jpg(file_path: Path, save_dir: Path) -> list[Path]:
    """Transform PDF files to page-wise JPG files

    Args:
        file_path (Path): path to a file to be inspected
        save_dir (Path): path to a directory to save output images

    Returns:
        list[Path]: a list of resulting page-wise images
    """
    save_dir.mkdir(parents=True, exist_ok=True)
    filename = Path(file_path).stem

    image_paths = []

    # Convert PDF into separate pages
    with tempfile.TemporaryDirectory() as path:
        images = convert_from_path(file_path, output_folder=path)

        for idx, image in enumerate(images):
            save_path = Path(save_dir, f"{filename}_page_{idx}.jpg")
            image.save(save_path, "JPEG")
            image_paths.append(save_path)

    return image_paths


async def run_inference(agent: Agent, prompt: str, image_path: Path) -> Results:
    """Run inference with `agent` using `prompt` and `image_path`.

    Args:
        agent (Agent): an Agent or LLM model used to run the inference with
        prompt (str): textual analysis instructions for the Agent/LLM model
        image_path (Path): path to the analyzed image

    Returns:
        Results: Pydantic object containing filename and analysis result data
    """
    async with semaphore:
        message_parts = [prompt, BinaryContent(data=image_path.read_bytes(), media_type="image/jpeg")]

        analysis_result = await agent.run(message_parts)
        log.info(f"File analyzed: {image_path.stem}")

        # Optional - uncomment line below to see the structured output
        # of model's analysis
        ic(analysis_result.output)
        output = Results(filename=image_path.stem, result=analysis_result.output)
        return output


async def analyze_each_page(image_paths: list[Path]) -> list[Results]:
    """Method analyzing each page/image from provided list

    Args:
        image_paths (list[Path]): a list of images to be analyzed

    Returns:
        list[Results]: a list of Results objects containing analysis results
    """
    # Run all tasks in parallel
    tasks = [run_inference(agent, prompt, path) for path in image_paths]
    results_objects = await asyncio.gather(*tasks)

    return [r.model_dump() for r in results_objects]


async def save_results_to_json(base_filename: str, results: list[Results], save_dir: Path) -> None:
    """Saves analysis result to JSON file.

    Args:
        base_filename (str): filename of the base file (the one analysis started from)
        results (list[Results]): a list of Results objects (one per page)
        save_dir (Path): directory to save the resulting JSON file
    """
    save_dir.mkdir(parents=True, exist_ok=True)
    save_path = Path(save_dir, f"{base_filename}.json")
    with open(save_path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=4, ensure_ascii=False)


async def main():
    pdf_dir = Path("./files/samples/")
    temp_dir = Path("./files/temp_files")
    results_dir = Path("./files/results")
    pdf_paths = await list_all_files(pdf_dir)

    for pdf_path in pdf_paths:
        image_paths = await pdf_to_jpg(pdf_path, temp_dir)
        results = await analyze_each_page(image_paths)
        await save_results_to_json(pdf_path.stem, results, results_dir)


if __name__ == "__main__":
    start_time = time.perf_counter()
    try:
        asyncio.run(main())
    except Exception as e:
        log.exception(e)

    end_time = time.perf_counter() - start_time
    log.info(f"Analysis took: {end_time:.1f} seconds")
