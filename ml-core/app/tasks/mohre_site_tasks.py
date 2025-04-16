import os
import asyncio
from celery import shared_task

from llama_index.core import Document

from app.models.document_metadata import DocumentMetadata
from app.core.config import settings, firecrawl_app
from app.scrapers.mohre_scraper import (
    scrape_mohre_faqs,
    get_docs_download_data,
    get_mohre_services_urls,
)
from app.core.llm.splitters import splitter_manager
from app.core.llm.rephrase import rephrase_manager
from app.core import constants
from app.dependencies.chroma_repo import get_chroma_repository
from app.utils import comm_func


@shared_task(name="download_mohre_docs", bind=True, max_retries=None)
def download_mohre_docs(self):
    try:
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

            # Download files
            comm_func.download_files(
                urls=[d["link"] for d in data],
                filenames=[d["description"] for d in data],
                destination_folder=download_folder,
                allow_exts=["pdf"],
            )

            for file in os.listdir(download_folder):
                title = file.split(".")[0]
                metadata = DocumentMetadata(source_url=url, title=title, is_file=True)

                nodes = splitter_manager.markdown_splitter(
                    docs=[comm_func.pdf_to_markdown(f"{download_folder}/{file}")],
                    metadata=metadata.to_dict(),
                )

                chroma_repo.add_node_to_collection(nodes)

            # Remove the temp download folder
            comm_func.delete_folder(download_folder)

        return True
    except:
        self.retry(countdown=2 * 60 * 60)
        return False


@shared_task(name="get_mohre_faq", bind=True, max_retries=None)
def get_mohre_faq(self):
    try:
        chroma_repo = get_chroma_repository(settings.MOHRE_DOC_CHROMA_COLLECTION)

        chroma_repo.delete_document_by_metadata(
            DocumentMetadata.to_filter_dict(source_url=constants.MOHRE_FAQ_URL)
        )

        topics, questions, answers = scrape_mohre_faqs()
        for topic, question, answer in zip(topics, questions, answers):
            metadata = DocumentMetadata(
                source_url=constants.MOHRE_FAQ_URL, title=question, is_file=False
            )
            rephased = rephrase_manager.rephrase_mohre_faq(topic, question, answer)
            document = Document(text=rephased, metadata=metadata.to_dict())
            chroma_repo.add_document_to_collection(document)
    except:
        self.retry(countdown=2 * 60 * 60)
        return


@shared_task(name="get_mohre_services", bind=True, max_retries=None)
def get_mohre_services(self):
    try:
        chroma_repo = get_chroma_repository(settings.MOHRE_DOC_CHROMA_COLLECTION)
        urls = get_mohre_services_urls()

        chroma_repo.delete_document_by_metadata(
            DocumentMetadata.to_filter_dict(source_url=constants.MOHRE_SERVICES_URL)
        )
 
        for url in urls:
            data = firecrawl_app.scrape_url(url, params={"formats": ["markdown"]})
            metadata = DocumentMetadata(
                source_url=url, title=data["metadata"]["title"], is_file=False
            )
            nodes = splitter_manager.markdown_splitter(
                [data["markdown"]], metadata=metadata.to_dict()
            )

            chroma_repo.add_node_to_collection(nodes)
    except:
        self.retry(countdown=2 * 60 * 60)
