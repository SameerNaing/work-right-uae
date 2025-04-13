import requests
from bs4 import BeautifulSoup

from app.core import constants

from .base_scraper import playwright


@playwright
async def get_mohre_services_urls(playwright, **kwargs) -> list[str]:
    """Function to get MOHRE Services URLs

    Returns:
        list[str]: list of services urls
    """

    webkit = playwright.webkit
    browser = await webkit.launch(headless=True)
    context = await browser.new_context()
    page = await context.new_page()
    await page.goto(constants.MOHRE_SERVICES_URL)

    services_count = page.locator(".fi-pageme-info")
    services_count = await services_count.inner_text()
    services_count = int(services_count.split(" ")[-1])
    services_link = []

    done_button = page.locator('a.introjs-button.introjs-skipbutton[title="Done"]')
    await page.wait_for_selector(
        'a.introjs-button.introjs-skipbutton[title="Done"]', state="visible"
    )
    await done_button.click()

    accept_button = page.locator('a.more.close[title="موافق / Accept"]')
    await page.wait_for_selector(
        'a.more.close[title="موافق / Accept"]', state="visible"
    )
    await accept_button.click()

    next_button = page.locator('a[href="#"][class="fi-arrow-right"][title="Next"]')
    await page.wait_for_selector(
        'a[href="#"][class="fi-arrow-right"][title="Next"]', state="visible"
    )

    for i in range(services_count):
        await page.locator(".fi-pageme-loading").wait_for(state="hidden")
        await next_button.click()

    anchors = page.locator('a:has-text("View Details")')
    count = await anchors.count()

    for i in range(count):
        href = await anchors.nth(i).get_attribute("href")
        services_link.append(href)

    return [f"{constants.MOHRE_URL}/{i}" for i in services_link]


def scrape_mohre_faqs() -> tuple[list[str], list[str], list[str]]:
    """Function to scrape MOHRE FAQs

    Returns:
        topics, questions, answers: tuple of lists of topics, questions and answers
    """
    html = requests.get(constants.MOHRE_FAQ_URL).text

    soup = BeautifulSoup(html, "html.parser")

    faq_div = soup.select("div.faq")[0]

    sections = BeautifulSoup(str(faq_div), "html.parser").find_all(
        "h3", class_="clearfix"
    )

    topics = []
    questions = []
    answers = []

    for section in sections:
        ul_tag = section.find_next_sibling("ul")
        for li in ul_tag.find_all("li", recursive=False):
            question = (
                li.find("a").get_text(strip=True)
                if li.find("a")
                else "No question found"
            )
            answer = (
                li.find("div", class_="details").get_text(strip=True)
                if li.find("p")
                else "No answer found"
            )
            topics.append(section.get_text(strip=True))
            questions.append(question)
            answers.append(answer)

    return topics, questions, answers


@playwright
async def get_docs_download_data(playwright, url, **kwargs) -> list[dict]:
    """Function to get docs download data

    Args:
        url (str): URL to download documents

    Returns:
        list[dict]: list of dictionaries containing description and link {description: str, link: str}
    """
    browser = await playwright.chromium.launch(headless=True)
    page = await browser.new_page()

    await page.goto(url)

    await page.wait_for_selector("tbody")

    rows = await page.query_selector_all("tbody tr.data")

    data = []
    for row in rows:
        description = await row.eval_on_selector(
            "td:nth-child(2) h4", "el => el.innerText"
        )
        link = await row.eval_on_selector("td:nth-child(4) a", "el => el.href")
        data.append({"description": description, "link": link})

    await browser.close()

    return data
