import pymupdf
import pymupdf4llm
from src.core import logging


def pdf_file_name_to_md(file_name: str) -> str:
    logging.logger.info("Filename", file_name)
    # Read and only select pages that contains the table
    doc = pymupdf.open(file_name)
    pages_to_consider = []
    for page in doc:
        if "Lead-Based Paint Testing Data Report" in page.get_text():
            pages_to_consider.append(page.number)

    # convert the selected page into markdown
    md_text = pymupdf4llm.to_markdown(
        file_name,
        pages=pages_to_consider,
        ignore_images=True,
        ignore_graphics=True,
        table_strategy="lines",
    )

    return md_text
