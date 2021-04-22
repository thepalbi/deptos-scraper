import requests
from bs4 import BeautifulSoup
from hashlib import sha1
from urllib.parse import urlparse
from dataclasses import dataclass
from typing import List, TextIO
import json
import logging

logging.basicConfig(level=logging.INFO)


@dataclass
class Parser:
    website: str
    link_regex: str

    def extract_links(self, contents: str):
        soup = BeautifulSoup(contents, "lxml")
        ads = soup.select(self.link_regex)
        for ad in ads:
            href = ad["href"]
            _id = sha1(href.encode("utf-8")).hexdigest()
            yield {"id": _id, "url": "{}{}".format(self.website, href)}


@dataclass
class Configuration:
    seen_file: str
    parsers: List[Parser]
    urls: List[str]
    telegram_key: str
    telegram_room_id: str


configuration: Configuration = None


def from_config_file(file_ptr: TextIO):
    logging.info("Reading raw configuration file")
    c = json.load(file_ptr)

    app_c = c["app"]

    parsers = [Parser(parser_c["website"], parser_c["link_regex"])
               for parser_c in app_c["parsers"]]
    logging.info("Registered %d parsers", len(parsers))

    tlg_c = c["telegram"]

    return Configuration(
        app_c["seen_file"],
        parsers,
        app_c["urls"],
        tlg_c["key"],
        tlg_c["room_id"]
    )


def _bootstrap() -> Configuration:
    logging.info("Opening configuration file")
    try:
        with open("Config.json", "r") as f:
            return from_config_file(f)
    except Exception as e:
        logging.fatal("Failed to bootstrap scraper. Cause: %s", e)
        raise Exception("failed to bootstrap scraper")


def _main():
    for url in configuration.urls:
        res = requests.get(url)
        ads = list(extract_ads(url, res.text))
        seen, unseen = split_seen_and_unseen(ads)

        logging.info("%d seen, %d unseen", len(seen), len(unseen))

        for u in unseen:
            # notify(u)
            print(u)

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
    bot = "YOUR_BOT_ID"
    room = "YOUR_CHAT_ROOM_ID"
    url = "https://api.telegram.org/bot{}/sendMessage?chat_id={}&text={}".format(
        bot, room, ad["url"])
    r = requests.get(url)


def mark_as_seen(unseen):
    with open(configuration.seen_file, "a+") as f:
        ids = ["{}\n".format(u["id"]) for u in unseen]
        f.writelines(ids)


if __name__ == "__main__":
    logging.info("Starting scraper")

    configuration = _bootstrap()
    logging.info("Scraper bootstraped successfully. Running!")

    _main()
