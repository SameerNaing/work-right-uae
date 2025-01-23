import os
import time
import shutil
import asyncio
import requests
from celery import shared_task


from app.models.document_metadata import DocumentMetadata
from app.core.config import settings
from app.scrapers.mohre_scraper import scrape_mohre_faqs, get_docs_download_data
from app.core.ai.llms import rephase_faq, splitters
from app.core import constants
from app.db.vector_store import get_vector_store
from app.dependencies.chroma_repo import get_chroma_repository
from .base_task import BaseTask


@shared_task(name="download_mohre_docs", bind=True, max_retries=None)
def download_mohre_docs(self):
    chroma_repo = get_chroma_repository(settings.MOHRE_DOC_CHROMA_COLLECTION)

    download_folder = "./download"

    for url in [
        constants.MOHRE_DOC_LAWS_URL,
        constants.MOHRE_DOC_RESOLUTION_CIRCULARS_URL,
        constants.MOHRE_DOC_INTERNATIONAL_AGREE_ULR,
    ]:
        # Remove old data from chroma db
        chroma_repo.delete_document_by_metadata(
            DocumentMetadata.to_filter_dict(source_url=url)
        )

        data = asyncio.run(get_docs_download_data(url=url))

        _download_docs(
            urls=[d["link"] for d in data], filenames=[d["description"] for d in data]
        )

        for file in os.listdir(download_folder):
            metadata = DocumentMetadata(source_url=url, title=file, is_file=True)

        break
    return True


@shared_task(name="get_mohre_faq", bind=True, max_retries=None, base=BaseTask)
def get_mohre_faq(self):
    try:
        topics, questions, answers = scrape_mohre_faqs()
        documents = rephase_faq.rephase(topics, questions, answers)
        vec = get_vector_store("mohre_faq")
        vec.delete()

    except:
        self.retry(countdown=2 * 60 * 60)
        return


def _download_docs(urls, filenames, destination_folder):

    for url, filename in zip(urls, filenames):
        response = requests.get(url, stream=True)
        ext = (
            response.headers.get("Content-Disposition")
            .split("filename=")[-1]
            .split(".")[-1]
        )

        if ext != "pdf":
            continue

        filename = f"{filename}.{ext}"

        if not os.path.exists(destination_folder):
            os.makedirs(destination_folder)

        with open(os.path.join(destination_folder, filename), "wb") as file:
            for chunk in response.iter_content(chunk_size=128):
                file.write(chunk)
