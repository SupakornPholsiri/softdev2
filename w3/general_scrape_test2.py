import requests
from bs4 import BeautifulSoup
from pythainlp import word_tokenize
import csv
import re

class Scraper:

    def generate_soup(self, url):
        self.url = url
        html = requests.get(url)
        print(html.text)
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
        pattern = re.compile(r'[\n/,.\[\]()_:;/?! ‘\xa0©=“”{}%_&<>’\|"]')
        for token in tokens:
            if not token or pattern.match(token):
                continue
            if token not in self.index:
                self.index[token] = [url]
            elif url not in self.index[token]:
                self.index[token].append(url)

        return self.index

    def save_to_file(self):
        with open('index.csv', 'w', encoding="utf-8") as f:
            for key in self.index.keys():
                f.write(f'"{key}","{self.index[key]}"\n')
        f.close()

    def read_file(self):
        #Temporary used for output testing.
        with open('index.csv', 'r', encoding="utf-8") as f:
            filecontent = csv.reader(f)
            self.index = {row[0]:eval(row[1]) for row in filecontent}
        f.close()

class Spider:
    queue = []
    crawled = []
    
    def __init__(self, base_url, depth = None):
        self.depth = depth
        self.generate_soup(base_url)
        self.add_links_to_queue(self.get_links())
        Spider.crawled.append(base_url)

    def get_base_domain(self, url):
        return "/".join(url.split("/")[0:3])

    def add_links_to_queue(self, links):
        for link in links:
            if link in Spider.crawled:
                continue
            Spider.queue.append(link)

    def crawl(self, link):
        self.generate_soup(link)
        self.add_links_to_queue(self.get_links())
        Spider.crawled.append(link)
        return self.get_text()

    def generate_soup(self, url):
        self.url = url
        self.base_domain = self.get_base_domain(self.url)
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
            href = link_html['href']
            if not href:
                continue
            if href.startswith("//"):
                continue #links.add(f'https:{link_html["href"]}')
            elif href.startswith("/"):
                links.add(f'{"/".join(self.url.split("/")[0:3])}{link_html["href"]}')
            elif href.startswith("./"):
                links.add(f'{self.url}{link_html["href"][1:]}')
            elif href.startswith("https://"):
                if self.get_base_domain(href) == self.base_domain:
                    links.add(href)
        return links


if __name__ == "__main__":
    spider = Spider("https://iot-kmutnb.github.io/blogs")
    index = Index()
    print(Spider.queue, end = "\n------------------------------------------\n")
    print(Spider.crawled)
    while len(Spider.queue) > 0:
        index.modify_index_with_tokens(word_tokenize(spider.crawl(Spider.queue.pop())), spider.url)
    index.save_to_file()
    #scraper = Scraper()
    #index = Index()
    #scraper.generate_soup("https://www.thairath.co.th")
    #index.modify_index_with_tokens(word_tokenize(scraper.get_text()), scraper.url)
    #scraper.generate_soup("https://www.blog.datahut.co/post/how-to-build-a-web-crawler-from-scratch")
    #index.modify_index_with_tokens(word_tokenize(scraper.get_text()), scraper.url)
    #index.save_to_file()
    #index.read_file()
    #for i in index.index:
        #print(i, index.index[i])

