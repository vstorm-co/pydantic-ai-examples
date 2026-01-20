import asyncio
import json
import os
import tempfile
import time
from pathlib import Path

from dotenv import load_dotenv
from loguru import logger as log
from pdf2image import convert_from_path
from pydantic import BaseModel, Field
from pydantic_ai import Agent, BinaryContent
from pydantic_ai.models.openai import OpenAIChatModel
from pydantic_ai.settings import ModelSettings

load_dotenv()

# ==============================================================================
# CONCURRENCY CONTROL
# ==============================================================================
# Semaphore limits concurrent API calls to avoid overwhelming the LLM service.
# Max 5 simultaneous requests is a safe balance between speed and reliability.
# Adjust this value if you hit rate limits (reduce to 2-3) or want faster
# processing with a more generous API quota (increase to 10+).
semaphore = asyncio.Semaphore(5)


# ==============================================================================
# PYDANTIC MODELS - Define data structures and validation
# ==============================================================================
# These models serve two purposes:
# 1. Define the expected JSON schema for the API response
# 2. Provide automatic validation - Pydantic will reject invalid data from the LLM
class Results(BaseModel):
    """Wrapper for basic OCR results - just filename and text output"""

    filename: str = ""
    result: str = ""


class FileElement(BaseModel):
    """Represents a single element detected on a document page.

    Examples of elements:
    - A table with columns and rows
    - A paragraph of text
    - An image or logo description
    - A header or title
    - A list or bullet points
    """

    element_type: str = Field(description="Type of the element found on the page", default="")
    element_content: str = Field(description="Content of the element found on the page", default="")


class ModelAnalysisOutput(BaseModel):
    """Structured output from the LLM for document analysis.

    This is the schema that tells the LLM exactly what we want back.
    PydanticAI uses this to enforce type checking on LLM responses.
    """

    file_type: str = Field(
        description="Type name which can describe given file precisely, e.g.: invoice, internal_document, instruction, other",
        default="",
    )
    file_content_md: str = Field(description="Output of the OCR process, contents of the file in Markdown", default="")
    file_elements: list[FileElement] = Field(
        description="Elements the given page consists from: tables, images, paragraphs, graphs, flowcharts etc.", default_factory=list
    )


class OCROutput(BaseModel):
    """Final output combining the filename and structured analysis results."""

    filename: str = ""
    analysis_result: ModelAnalysisOutput = Field(default_factory=ModelAnalysisOutput)


# ===== CONFIGURATION 1: Basic Unstructured OCR =====
# This agent returns plain Markdown text without schema enforcement
model = OpenAIChatModel("gpt-5.1", settings=ModelSettings(temperature=0))
# Temperature=0 makes the model more deterministic and analytical (less creative)
# This is ideal for OCR since we want consistent, accurate text extraction
# Higher temps (0.5-1.0) would introduce randomness in output

agent = Agent(
    model=model,
    system_prompt="You are an OCR expert specialized in the data extraction \
        from various types of documents. You are always precise and make sure \
        that extraction is done properly.",
)

prompt = (
    # Core task instruction
    "Provided below you can find a document. "
    "Perform a full-scale OCR process on it. Return its content in the Markdown but **without** "
    "backticks used for usual code marking in the document itself. "
    # Guidance on quality and format
    "Do your best to provide original format and try to retain as much of original structure as possible. "
    "Use regular Markdown elements like tables, image descriptions, lists, headers and others. "
    # Constraint: Don't add extra processing
    "Do not perform any additional actions other than recognition of the characters "
    "in the document and translating it into a Markdown result."
)


# ==============================================================================
# UTILITY FUNCTIONS - Handle file operations and LLM inference
# ==============================================================================
def list_all_files(directory: Path, extension: str = "pdf") -> list[Path]:
    """Find all files with a specific extension in a directory.

    Args:
        dir (Path): directory to be checked
        extension (str, optional): file extension of files to be listed. Defaults to "pdf".

    Returns:
        list[Path]: a list of filepaths for further analysis
    """
    return [Path(directory, f) for f in os.listdir(directory) if f.lower().endswith(extension)]


def pdf_to_jpg(file_path: Path, save_dir: Path) -> list[Path]:
    """Convert PDF pages to individual JPG images.

    PDFs are converted to images because:
    - LLMs process images better than PDF binary data
    - Each page becomes a separate analysis task (better for scaling)
    - JPG format is more compatible with image APIs

    Args:
        file_path (Path): path to a file to be inspected
        save_dir (Path): path to a directory to save output images

    Returns:
        list[Path]: a list of resulting page-wise images
    """
    save_dir.mkdir(parents=True, exist_ok=True)
    filename = Path(file_path).stem

    image_paths = []

    # Use temporary directory to avoid cluttering the save directory with intermediate files
    # convert_from_path returns PIL Image objects, we save them as JPG
    with tempfile.TemporaryDirectory() as path:
        images = convert_from_path(file_path, output_folder=path)

        for idx, image in enumerate(images):
            save_path = Path(save_dir, f"{filename}_page_{idx}.jpg")
            image.save(save_path, "JPEG")
            image_paths.append(save_path)

    return image_paths


async def run_inference(agent: Agent, prompt: str, image_path: Path) -> Results | OCROutput:
    """Execute LLM inference on a single document image.

    This is the core function that:
    1. Reads the image file
    2. Sends it to the LLM with the prompt
    3. Handles any errors
    4. Returns the result in the appropriate format

    Args:
        agent (Agent): an Agent or LLM model used to run the inference with
        prompt (str): textual analysis instructions for the Agent/LLM model
        image_path (Path): path to the analyzed image

    Returns:
        Results | OCROutput: Pydantic object containing filename and analysis result data
    """
    async with semaphore:
        # BinaryContent wraps the image bytes with proper media type.
        # This tells PydanticAI that we're sending an image, not text.
        message_parts = [prompt, BinaryContent(data=image_path.read_bytes(), media_type="image/jpeg")]

        try:
            # Run the agent with the image and prompt.
            # The LLM analyzes the image according to the system_prompt and output_type.
            analysis_result = await agent.run(message_parts)
            log.info(f"File analyzed: {image_path.stem}")
        except Exception as e:
            log.warning(f"Unexpected error while inference: {e}")
            raise RuntimeError from e

        # Optional - uncomment line below to see the structured output
        # of model's analysis (useful for debugging)
        # ic(analysis_result.output)

        # The output format depends on whether we used structured output:
        # - If ModelAnalysisOutput: Wrap in OCROutput with filename
        # - If unstructured: Wrap in Results with filename
        if isinstance(analysis_result.output, ModelAnalysisOutput):
            output = OCROutput(filename=image_path.stem, analysis_result=analysis_result.output)
        else:
            output = Results(filename=image_path.stem, result=analysis_result.output)
        return output


async def analyze_each_page(agent: Agent, prompt: str, image_paths: list[Path]) -> list[Results]:
    """Analyze multiple images in parallel using asyncio.gather().

    This leverages async/await to process multiple pages concurrently,
    significantly faster than processing them one by one.
    The semaphore prevents overwhelming the API with too many requests.

    Args:
        agent (Agent): an Agent to perform the analysis
        prompt (str): prompt used for the analysis
        image_paths (list[Path]): a list of images to be analyzed

    Returns:
        list[Results]: a list of Results objects containing analysis results
    """
    # Run all tasks in parallel using asyncio.gather()
    # This is much faster than awaiting each task sequentially
    # asyncio.gather() waits for all tasks to complete and returns results in order
    tasks = [run_inference(agent, prompt, path) for path in image_paths]
    results_objects = await asyncio.gather(*tasks)

    return [r.model_dump() for r in results_objects]


async def save_results_to_json(prefix: str | None, base_filename: str, results: list[Results], save_dir: Path) -> None:
    """Save analysis results to a JSON file.

    Each analysis produces a JSON file with all the extracted data.
    This allows further processing or archiving of results.

    Args:
        prefix (str | None): prefix to be used for saved files (e.g., 'structured')
        base_filename (str): filename of the base file (the one analysis started from)
        results (list[Results]): a list of Results objects (one per page)
        save_dir (Path): directory to save the resulting JSON file
    """
    save_dir.mkdir(parents=True, exist_ok=True)
    if prefix:
        base_filename = f"{prefix}_{base_filename}"

    save_path = Path(save_dir, f"{base_filename}.json")
    # Use ensure_ascii=False to properly handle unicode characters from OCR
    with open(save_path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=4, ensure_ascii=False)


async def main_basic():
    """Main entry point for basic (unstructured) OCR processing.

    Workflow:
    1. Find all PDFs in ./files/samples/
    2. For each PDF: convert to JPG images (one per page)
    3. For each image: run LLM inference to extract text as Markdown
    4. Save results to JSON in ./files/results/

    Output format: Unstructured Markdown text in JSON
    """
    pdf_dir = Path("./files/samples/")
    temp_dir = Path("./files/temp_files")
    results_dir = Path("./files/results")
    pdf_paths = list_all_files(pdf_dir)

    for pdf_path in pdf_paths:
        # Convert PDF to individual page images
        image_paths = pdf_to_jpg(pdf_path, temp_dir)
        # Analyze each image with the unstructured agent
        results = await analyze_each_page(agent, prompt, image_paths)
        # Save results without prefix (basic results)
        await save_results_to_json(None, pdf_path.stem, results, results_dir)


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
