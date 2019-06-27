import requests
import pprint
from bs4 import BeautifulSoup
from collections import Counter
from multiprocessing import Pool
from time import clock


class PikabuGrabber:
    HOME = "https://pikabu.ru/subs"
    HEADERS_MAIN = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
        "cookie": "",
        "cache-control": "max-age=0",
        "referer": "https://pikabu.ru/",
        "upgrade-insecure-requests": "1",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36",
    }

    def __init__(self):
        self.session = requests.Session()
        self.get_cookie("cookie.txt")
        self.session.headers = self.HEADERS_MAIN
        self.counter_tags = Counter()

    def get_cookie(self, file: str):
        with open(file, "r") as f:
            cookie = f.read()
        self.HEADERS_MAIN["cookie"] = cookie

    def get_page(self, url: str):
        get = self.session.get(url).text
        # print(get)
        return get

    @staticmethod
    def get_links(html: str) -> list:
        soup = BeautifulSoup(html, "html.parser")
        titles = soup.find_all("h2", class_="story__title")
        print(len(titles))
        links = []
        for title in titles:
            info = title.find("a")
            links.append((info.get("href"), info.text.strip()))
        return links

    def get_info_about_post(self, link: tuple):
        print(link[1])
        html = self.get_page(link[0])
        soup = BeautifulSoup(html, "html.parser")
        tags = soup.find("div", class_="story__tags").find_all("a", class_="tags__tag")
        tags = list(map(lambda tag: tag.text.strip(), tags))
        self.counter_tags.update(tags)

    def get_next_page(self):
        url = "https://pikabu.ru/subs?twitmode=1&of=v2&page=2&_=1561642498805"


if __name__ == "__main__":
    grabber = PikabuGrabber()
    main_page_html = grabber.get_page(grabber.HOME)
    posts_links = grabber.get_links(main_page_html)  # кортеж (ссылка, имя)
    start = clock()
    for post_link in posts_links:
        grabber.get_info_about_post(post_link)
    end = clock()
    pprint.pprint(grabber.counter_tags)
    print(end-start)
    with open("tag_list.txt", "w") as f:
        for key, value in grabber.counter_tags.most_common(10):
            f.write(f"{key} {value}\n")
    # 112 сек. в одном потоке

    # start = clock()
    # with Pool() as p:
    #     p.map(grabber.get_info_about_post, posts_links, chunksize=4)
    # end = clock()
    # pprint.pprint(grabber.counter_tags)
    # print(end-start)
