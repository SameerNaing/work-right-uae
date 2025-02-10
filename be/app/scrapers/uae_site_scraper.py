from urllib.parse import urlparse


from app.core.config import firecrawl_app


class UAEWebsiteLinkScraper:
    def __init__(self, visited=[]):
        self.app = firecrawl_app
        self.error = False
        self.error_msg = None
        self.remaining_urls = []
        self.last_pages = []
        self.visited_pages = visited

    def _parse_url(self, url):
        parsed_url = urlparse(url)
        lang, info_service, section, *_ = parsed_url.path.strip("/").split("/")
        main_url = (
            f"{parsed_url.scheme}://{parsed_url.netloc}/{lang}/{info_service}/{section}"
        )
        return main_url

    def _clean_url(self, url):
        parsed_url = urlparse(url)
        return f"{parsed_url.scheme}://{parsed_url.netloc}{parsed_url.path}"

    def _filter_urls(self, base_url, links):
        if base_url.endswith("*"):
            base_url = base_url[:-1]

        return [link for link in links if link.startswith(base_url)]

    def _scrape_links(self, url):
        data = self.app.scrape_url(url, params={"formats": ["links"]})
        return data["links"]

    def result(self):
        return {
            "error": self.error,
            "error_msg": self.error_msg,
            "remaining_urls": self.remaining_urls,
            "last_pages": self.last_pages,
            "visited_pages": self.visited_pages,
        }

    def crawl_urls(self, urls=[]):
        try:
            if len(urls) == 0:
                return

            url = urls[0]

            main_url = self._parse_url(url)

            links = self._scrape_links(url)
            links = list(set([self._clean_url(link) for link in links]))
            links = self._filter_urls(f"{main_url}/*", links)
            links = [link for link in links if link not in self.visited]
            links = [link for link in links if link not in urls]

            urls = urls[1:] + links

            sub_pages = self._filter_urls(f"{url}/*", links)

            if len(sub_pages) == 0:
                self.last_pages.append(url)

            self.visited.append(url)

            return self.crawl_urls(urls)

        except Exception as e:
            self.error = True
            self.error_msg = str(e)
            self.remaining_urls = urls
            return
