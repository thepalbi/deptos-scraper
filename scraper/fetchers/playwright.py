from os import stat
from playwright.sync_api import sync_playwright, Response
from scraper.fetchers.api import FetcherResponse


class PlaywrightFetcher:
    def __init__(self) -> None:
        pass

    def get(self, url: str) -> FetcherResponse:
        fetcher_res = FetcherResponse(200, "")

        def handle_req_finished(res: Response):
            if res.request.url == url:
                fetcher_res.status_code = res.status

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=False)
            page = browser.new_page()
            page.goto(url)
            page.on("response", handle_req_finished)
            fetcher_res.text = page.content()
            browser.close()

        return fetcher_res
