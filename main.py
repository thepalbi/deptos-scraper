import requests
from bs4 import BeautifulSoup
from hashlib import sha1
from urllib.parse import urlparse
from dataclasses import dataclass

urls = {
    "https://www.argenprop.com/departamento-alquiler-barrio-palermo-barrio-belgrano-barrio-colegiales-barrio-villa-crespo-2-ambientes-y-3-ambientes-25000-75000-pesos-1-o-m%c3%a1s-cocheras-desde-45-m2-cubiertos-con-ambiente-balcon-orden-masnuevos"
}


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


parsers = [
    Parser(website="https://www.zonaprop.com.ar", link_regex="a.go-to-posting"),
    Parser(website="https://www.argenprop.com", link_regex="div.listing__items div.listing__item a"),
    Parser(website="https://inmuebles.mercadolibre.com.ar", link_regex="li.results-item .rowItem.item a"),
]


def _main():
    for url in urls:
        res = requests.get(url)
        ads = list(extract_ads(url, res.text))
        seen, unseen = split_seen_and_unseen(ads)

        print("{} seen, {} unseen".format(len(seen), len(unseen)))

        for u in unseen:
            # notify(u)
            print(u)

        mark_as_seen(unseen)


def extract_ads(url, text):
    uri = urlparse(url)
    parser = next(p for p in parsers if uri.hostname in p.website)
    return parser.extract_links(text)


def split_seen_and_unseen(ads):
    history = get_history()
    seen = [a for a in ads if a["id"] in history]
    unseen = [a for a in ads if a["id"] not in history]
    return seen, unseen


def get_history():
    try:
        with open("seen.txt", "r") as f:
            return {l.rstrip() for l in f.readlines()}
    except:
        return set()


def notify(ad):
    bot = "YOUR_BOT_ID"
    room = "YOUR_CHAT_ROOM_ID"
    url = "https://api.telegram.org/bot{}/sendMessage?chat_id={}&text={}".format(bot, room, ad["url"])
    r = requests.get(url)


def mark_as_seen(unseen):
    with open("seen.txt", "a+") as f:
        ids = ["{}\n".format(u["id"]) for u in unseen]
        f.writelines(ids)


if __name__ == "__main__":
    _main()