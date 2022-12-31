import requests
from bs4 import BeautifulSoup

class Scraper:

    def generate_soup(self, url):
        self.url = url
        html = requests.get(url)
        self.soup = BeautifulSoup(html.text, "html.parser")

    def get_text(self):
        text = self.soup.text.lower()
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

class Spider:
    def __init__():
        

scraper = Scraper()
scraper.generate_soup("https://www.blog.datahut.co/post/how-to-build-a-web-crawler-from-scratch")
print(scraper.get_text())
print(scraper.get_links())
scraper.generate_soup("https://www.xn--42c2bf1bzl.com/blogs")
print(scraper.get_text())
print(scraper.get_links())