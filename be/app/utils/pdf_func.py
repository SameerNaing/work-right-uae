import pymupdf4llm


def pdf_to_markdown(file):
    return pymupdf4llm.to_markdown(file)
