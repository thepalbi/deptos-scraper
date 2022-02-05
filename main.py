import requests
from bs4 import BeautifulSoup
from hashlib import sha1
from urllib.parse import urlparse
from dataclasses import dataclass
from typing import List, TextIO
import json
import logging
import argparse
import cloudscraper

parser = argparse.ArgumentParser(description="Deptos scraper CLI")
parser.add_argument("--config", dest="config_file", required=True,
                    type=str, help="Path to the configuration file")
parser.add_argument("--log", dest="logging_file",
                    required=True, type=str, help="Path to the log file")


args = parser.parse_args()


def _bootstrap_logger(log_file):
    log = logging.getLogger("app")
    log.setLevel(logging.DEBUG)

    fh = logging.FileHandler(log_file)
    fh.setLevel(logging.DEBUG)

    ch = logging.StreamHandler()
    ch.setLevel(logging.ERROR)

    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)

    log.addHandler(fh)
    log.addHandler(ch)

    return log


log = _bootstrap_logger(args.logging_file)
scraper = cloudscraper.create_scraper()


@dataclass
class Parser:
    website: str
    # TODO: Rename this to link_css_path or sth like that!
    link_regex: str

    def extract_links(self, contents: str):
        soup = BeautifulSoup(contents, "lxml")
        ads = soup.select(self.link_regex)
        for ad in ads:
            href = ad["href"]
            _id = sha1(href.encode("utf-8")).hexdigest()
            yield {"id": _id, "url": "{}{}".format(self.website, href)}


class Fetcher:
    # TODO: Add pagination inside the fetcher
    def __init__(self, website: str, has_agent_protection: bool = False):
        self.website = website
        self._get_website = scraper.get if has_agent_protection else requests.get

    def get(self, url: str):
        return self._get_website(url)


default_fetcher = Fetcher('default')


@dataclass
class Configuration:
    seen_file: str
    parsers: List[Parser]
    fetchers: List[Fetcher]
    urls: List[str]
    telegram_key: str
    telegram_room_id: str
    telegram_notifier_enabled: bool


configuration: Configuration = None


def from_config_file(file_ptr: TextIO):
    log.info("Reading raw configuration file")

    c = json.load(file_ptr)
    app_c = c["app"]
    tlg_c = c["telegram"]

    parsers = [Parser(parser_c["website"], parser_c["link_regex"])
               for parser_c in app_c["parsers"]]
    log.info("Registered %d parsers", len(parsers))

    fetchers = [Fetcher(fetcher_c["website"], fetcher_c["has_agent_protection"])
                for fetcher_c in app_c["fetchers"]]
    log.info("Registered %d fetchers", len(parsers))

    return Configuration(
        app_c["seen_file"],
        parsers,
        fetchers,
        app_c["urls"],
        tlg_c["key"],
        tlg_c["room_id"],
        tlg_c["enabled"]
    )


def _bootstrap(config_file) -> Configuration:
    log.info("Opening configuration file: %s", config_file)
    try:
        with open(config_file, "r") as f:
            return from_config_file(f)
    except Exception as e:
        log.fatal("Failed to bootstrap scraper. Cause: %s", e)
        raise Exception("failed to bootstrap scraper")


def _main():
    log.info("Fetching from %d sources", len(configuration.urls))

    for url in configuration.urls:
        # Find applicable fetcher
        uri = urlparse(url)
        fetcher = next(
            (f for f in configuration.fetchers if uri.hostname in f.website), default_fetcher)

        res = fetcher.get(url)
        ads = list(extract_ads(url, res.text))
        seen, unseen = split_seen_and_unseen(ads)

        log.info("%d seen, %d unseen", len(seen), len(unseen))

        for u in unseen:
            log.debug("new depto: %s", u)
            if configuration.telegram_notifier_enabled:
                notify(u)

        mark_as_seen(unseen)


def extract_ads(url, text):
    uri = urlparse(url)
    parser = next(
        p for p in configuration.parsers if uri.hostname in p.website)
    return parser.extract_links(text)


def split_seen_and_unseen(ads):
    history = get_history()
    seen = [a for a in ads if a["id"] in history]
    unseen = [a for a in ads if a["id"] not in history]
    return seen, unseen


def get_history():
    try:
        with open(configuration.seen_file, "r") as f:
            return {l.rstrip() for l in f.readlines()}
    except:
        return set()


def notify(ad):
    url = "https://api.telegram.org/bot{}/sendMessage?chat_id={}&text={}".format(
        configuration.telegram_key, configuration.telegram_room_id, ad["url"])
    r = requests.get(url)


def mark_as_seen(unseen):
    with open(configuration.seen_file, "a+") as f:
        ids = ["{}\n".format(u["id"]) for u in unseen]
        f.writelines(ids)


if __name__ == "__main__":
    log.info("Starting scraper")

    configuration = _bootstrap(args.config_file)
    log.info("Scraper bootstraped successfully. Running!")

    _main()
