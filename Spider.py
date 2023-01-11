from bs4 import BeautifulSoup
import requests

class Spider:
    #The web crawler
    queue = []
    crawled = []
    
    #Create the spider with url as starting point
    def __init__(self, url, depth = None):
        self.depth = depth
        if url not in Spider.queue and url not in Spider.crawled:
            Spider.queue.append(url)

    #Get base domain from any url
    def get_base_domain(self, url):
        return "/".join(url.split("/")[0:3])

    #Add links gained from scraping to queue
    def add_links_to_queue(self):
        links = self.get_links()
        for link in links:
            if link in Spider.crawled or link in Spider.queue or link == self.url:
                continue
            Spider.queue.append(link)

    #Scrape the links and text from website
    def crawl(self, link):
        self.add_links_to_queue()
        Spider.crawled.append(link)
        return self.get_text()

    #Create the BeautifulSoup object and set url and base domain
    def generate_soup(self, url):
        self.url = url
        self.base_domain = self.get_base_domain(self.url)
        html = requests.get(url)
        self.soup = BeautifulSoup(html.text, "html.parser")
        
    #Get text from website
    def get_text(self):
        text = ""
        texts = self.soup.find_all(text = True)
        for i in texts:
            text = f"{text} {i.text.lower()}"
        return text

    def parse_url(self, url:str, base_url:str):
        if url[0] == "/": base_url = self.get_base_domain(base_url)
        splited_url = url.split("/")
        splited_base = base_url.split("/")
        new_abs_url = ""
        to_join = []
        current = -1
        for i in range(len(splited_url)):
            if splited_url[i] == "..":
                while current not in to_join and current > -1: current -= 1
                if current in to_join:
                    to_join.pop()
                elif current == -1 and len(splited_base) > 3: splited_base.pop()
            elif splited_url[i] != "." and splited_url[i] != "":
                to_join.append(i)
                current += 1
        if "." in splited_url[-1] and splited_url[-1] != "." and splited_url[-1] != "..":
            splited_url.pop()
            to_join.pop()
        for i in to_join: new_abs_url = f"{new_abs_url}/{splited_url[i]}"
        return f"{'/'.join(splited_base)}{new_abs_url}"

    #Get links from a elements in html
    def get_links(self):
        links_html = self.soup.find_all("a", href = True)
        links = set()
        for link_html in links_html:
            href = link_html['href']
            if not href:
                continue
            if href == "." or href.startswith("#") or href[0] == "[":
                continue
            if href.startswith("//"):
                continue #links.add(f'https:{link_html["href"]}')
            if href.startswith("https://") or href.startswith("http://") :
                if self.get_base_domain(href) == self.base_domain:
                    links.add(href)
            else:
                links.add(self.parse_url(href, self.url))
        return links