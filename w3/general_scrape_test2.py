import requests
from bs4 import BeautifulSoup
from pythainlp import word_tokenize
import csv
from collections import Counter
import re

class Scraper:

    def generate_soup(self, url):
        self.url = url
        html = requests.get(url)
        self.soup = BeautifulSoup(html.text, "html.parser")

    def get_text(self):
        text = ""
        texts = self.soup.find_all(text = True)
        for i in texts:
            text = f"{text} {i.text.lower()}"
        return text

    def get_links(self):
        links_html = self.soup.find_all("a", href = True)
        links = set()
        for link_html in links_html:
            if not link_html['href']:
                continue
            if link_html['href'].startswith("//"):
                links.add(f'https:{link_html["href"]}')
            elif link_html['href'].startswith("/"):
                links.add(f'{"".join(self.url.split("/")[0:3])}{link_html["href"]}')
            elif link_html['href'].startswith("https://"):
                links.add(link_html['href'])
        return links

class Index:

    def __init__(self):
        self.index = {}

    def modify_index_with_tokens(self, tokens, url):
        pattern = re.compile(r"[\n/,.\[\]()_:;\?! ‘\xa0©=“”{}]")
        for token in tokens:
            if not token or pattern.match(token):
                continue
            if token not in self.index:
                self.index[token] = [url]
            elif url not in self.index[token]:
                self.index[token].append(url)

        return self.index

    def save_to_file(self):
        with open('index.csv', 'w') as f:
            for key in self.index.keys():
                f.write(f"{key}, {self.index[key]}\n")
        f.close()


scraper = Scraper()
index = Index()
scraper.generate_soup("https://www.blog.datahut.co/post/how-to-build-a-web-crawler-from-scratch")
index.modify_index_with_tokens(word_tokenize(scraper.get_text()), scraper.url)
index.save_to_file()

