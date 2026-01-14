import asyncio
import json
import os
import tempfile
from pathlib import Path

from dotenv import load_dotenv
from loguru import logger as log
from pdf2image import convert_from_path
from pydantic import BaseModel, Field
from pydantic_ai import Agent, BinaryContent
from pydantic_ai.models.openai import OpenAIChatModel
from pydantic_ai.settings import ModelSettings

load_dotenv()

### Setup asyncio boundaries
semaphore = asyncio.Semaphore(5)


### Structures and Models
# Structure for saving final results in JSON file
class Results(BaseModel):
    filename: str = ""
    result: str = ""


class FileElement(BaseModel):
    element_type: str = Field(description="Type of the element found on the page", default="")
    element_content: str = Field(description="Content of the element found on the page", default="")


class ModelAnalysisOutput(BaseModel):
    file_type: str = Field(
        description="Type name which can describe given file precisely, i.ex.: invoice, internal_document, instruction, other",
        default="",
    )
    file_content_md: str = Field(description="Output of the OCR process, contents of the file in Markdown", default="")
    file_elements: list[FileElement] = Field(
        description="Elements the given page consists from: tables, images, paragraphs, graphs, flowcharts etc.", default_factory=list
    )


class OCROutput(BaseModel):
    filename: str = ""
    analysis_result: ModelAnalysisOutput = Field(default_factory=ModelAnalysisOutput)


### Create and setup PydanticAI agent
# Model's temperature is set to `0` for model to be more analytic
# in its work (less temperature = less creativity)

# Basic inference model
model = OpenAIChatModel("gpt-4o", settings=ModelSettings(temperature=0))
agent = Agent(
    model=model,
    system_prompt="You are an OCR expert specialized in the data extraction \
        from various types of documents. You are always precise and make sure \
        that extraction is done properly.",
)

prompt = (
    "Provided below you can find a document. "
    "Perform a full-scale OCR process on it. Return its content in the Markdown but **without** "
    "backticks used for usual code marking in the document itself. "
    "DO you best to provide original format and try to retain as much of original structure as possible. "
    "Use regular Markdown elements like tables, image descriptions, lists, headers and others. "
    "Do not perform any additional actions other than recognition of the characters "
    "in the document and translating it into a Markdown result."
)

# Model for inference with structured output
agent_structured = Agent(
    model=model,
    system_prompt="You are an OCR expert specialized in the data extraction \
        from various types of documents. You are always precise and make sure \
        that extraction is done properly.",
    output_type=ModelAnalysisOutput,
)

prompt_structured = (
    "You are an expert OCR and document analysis system. Provided below is a document. "
    "Your task is to analyze the document and return a structured JSON response following the schema:\n\n"
    "1. **file_type**: Identify the specific category of the document (e.g., invoice, internal_document, instruction). \n"
    "2. **file_content_md**: Perform a full-scale OCR. Convert the document into Markdown, "
    "retaining the original structure (tables, headers, lists). \n"
    "3. **file_elements**: Provide a granular list of elements found. For each element, "
    "specify its 'element_type' (e.g., table, image_description, paragraph) and its 'element_content'. \n\n"
    "Strictly perform character recognition and structural mapping. Do not add commentary or perform "
    "actions outside of translation into the requested schema."
)

prompt_warning = "Analyze the file and provide feedback."

agent_structured_wrong = Agent(
    model=model,
    system_prompt="You are an OCR expert specialized in the data extraction \
        from various types of documents. You are always precise and make sure \
        that extraction is done properly.",
    output_type=OCROutput,
)


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


async def run_inference(agent: Agent, prompt: str, image_path: Path) -> Results | OCROutput:
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

        try:
            analysis_result = await agent.run(message_parts)
            log.info(f"File analyzed: {image_path.stem}")
        except Exception as e:
            log.warning(f"Unexpected error while inference: {e}")
            raise RuntimeError from e

        # Optional - uncomment line below to see the structured output
        # of model's analysis
        # ic(analysis_result.output)

        # Different behavior depending on the output type provided
        # from the LLM/Agent
        if isinstance(analysis_result.output, ModelAnalysisOutput):
            output = OCROutput(filename=image_path.stem, analysis_result=analysis_result.output)
        else:
            output = Results(filename=image_path.stem, result=analysis_result.output)
        return output


async def analyze_each_page(agent: Agent, prompt: str, image_paths: list[Path]) -> list[Results]:
    """Method analyzing each page/image from provided list

    Args:
        agent (Agent): an Agent to perform the analysis
        prompt (str): prompt used for the analysis
        image_paths (list[Path]): a list of images to be analyzed

    Returns:
        list[Results]: a list of Results objects containing analysis results
    """
    # Run all tasks in parallel
    tasks = [run_inference(agent, prompt, path) for path in image_paths]
    results_objects = await asyncio.gather(*tasks)

    return [r.model_dump() for r in results_objects]


async def save_results_to_json(prefix: str | None, base_filename: str, results: list[Results], save_dir: Path) -> None:
    """Saves analysis result to JSON file.

    Args:
        prefix (str | None): prefix to be used for saved files
        base_filename (str): filename of the base file (the one analysis started from)
        results (list[Results]): a list of Results objects (one per page)
        save_dir (Path): directory to save the resulting JSON file
    """
    save_dir.mkdir(parents=True, exist_ok=True)
    if prefix:
        base_filename = f"{prefix}_{base_filename}"

    save_path = Path(save_dir, f"{base_filename}.json")
    with open(save_path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=4, ensure_ascii=False)


async def main_basic():
    pdf_dir = Path("./files/samples/")
    temp_dir = Path("./files/temp_files")
    results_dir = Path("./files/results")
    pdf_paths = await list_all_files(pdf_dir)

    for pdf_path in pdf_paths:
        image_paths = await pdf_to_jpg(pdf_path, temp_dir)
        results = await analyze_each_page(agent, prompt, image_paths)
        await save_results_to_json(None, pdf_path.stem, results, results_dir)


async def main_structured():
    pdf_dir = Path("./files/samples/")
    temp_dir = Path("./files/temp_files")
    results_dir = Path("./files/results")
    pdf_paths = await list_all_files(pdf_dir)

    for pdf_path in pdf_paths:
        image_paths = await pdf_to_jpg(pdf_path, temp_dir)
        results = await analyze_each_page(agent_structured, prompt_structured, image_paths)
        await save_results_to_json("structured", pdf_path.stem, results, results_dir)
