import os
import asyncio
from celery import shared_task

from app.scrapers.uae_site_scraper import UAEWebsiteLinkScraper
from app.core.config import firecrawl_app, settings
from app.dependencies.chroma_repo import get_chroma_repository
from app.models.document_metadata import DocumentMetadata
from app.core.llm.splitters import splitter_manager


@shared_task(name="crawl_uae_site_links", bind=True, max_retries=None)
def crawl_uae_site_links(self, urls=None, visited=[]):
    chroma_repo = get_chroma_repository(settings.MOHRE_DOC_CHROMA_COLLECTION)
    if urls is None:
        return

    scraper = UAEWebsiteLinkScraper(visited=visited)
    scraper.crawl_urls(urls=urls)

    result = scraper.result()

    if result["error"]:
        self.retry(
            countdown=2 * 60 * 60,
            kwargs={
                "urls": result["remaining_urls"],
                "visited": result["visited_pages"],
            },
        )
        return

    for url in result["last_pages"]:
        chroma_repo.delete_document_by_metadata(
            DocumentMetadata.to_filter_dict(source_url=url)
        )

        data = firecrawl_app.scrape_url(url, params={"formats": ["markdown"]})

        metadata = DocumentMetadata(
            source_url=url, title=data["metadata"]["title"], is_file=False
        )

        nodes = splitter_manager.markdown_splitter(data["markdown"], metadata.to_dict())
        chroma_repo.add_node_to_collection(nodes)
