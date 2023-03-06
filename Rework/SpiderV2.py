from queue import Queue
from bs4 import BeautifulSoup
import urllib.robotparser
import hashlib
import requests
class Spider:
    #The web crawler
    queue = []
    crawled = []
    base_domains = []
    all_robots = {}
    unaccessible_urls = []

    queue_front = 0
    queue_back = 1

    depth = 0
    max_depth = 2

    @classmethod
    def set_base_domains(cls, domains:list):
        """Set the domains that the spider will crawl to and read theirs robots.txt file"""
        cls.base_domains = [cls.get_base_domain(domain) for domain in domains]
        for domain in cls.base_domains:
            robots_url = f"https://{domain}/robots.txt"
            if requests.get(robots_url).status_code != 404:
                rp = urllib.robotparser.RobotFileParser()
                rp.set_url(robots_url)
                rp.read()
                Spider.all_robots[domain] = rp
            else:
                Spider.all_robots[domain] = None
        
    @classmethod
    def try_change_depth(cls):
        """Check for depth change when crawling through the web"""
        if cls.max_depth == cls.depth:
            return False
        if cls.queue_front == cls.queue_back+1:
            cls.depth += 1
            return True
        return False

    @classmethod
    def get_base_domain(cls, url:str):
        """Get base domain from any url"""
        return url.split("/")[2]
    
    def __init__(self, url=None):
        """Create a spider and add the url into queue"""
        if url == None:
            return
        if url not in Spider.queue and url not in Spider.crawled:
            Spider.queue.append(url)

    def add_links_to_queue(self):
        """Add links gained from scraping to queue"""
        links = self.get_links()
        for link in links:
            domain = self.get_base_domain(link)
            if domain in Spider.all_robots:
                if Spider.all_robots[domain] != None:
                    can_scrape = Spider.all_robots[self.get_base_domain(link)].can_fetch("*",link)
                else:
                    can_scrape = True
                if link in Spider.crawled or link in Spider.queue or link == self.url or not can_scrape:
                    continue
            Spider.queue.append(link)

    def crawl(self, hash_index:dict):
        """Scrape the links and text from website"""
        if self.url in hash_index:
            if hash_index[self.url] == self.hash :
                return None
        if Spider.max_depth > Spider.depth:
            self.add_links_to_queue()
        Spider.crawled.append(self.url)
        return (self.get_text(), list(self.get_links()), self.hash)

    def check_if_can_scrape(self, url:str):
        """Check if the spider should crawl the page"""
        if self.get_base_domain(url) not in Spider.base_domains:
            return False
        if Spider.all_robots[self.get_base_domain(url)] != None:
            can_scrape = Spider.all_robots[self.get_base_domain(url)].can_fetch("*",url)
        else:
            can_scrape = True
        if url not in Spider.queue or not can_scrape : 
            return False
        return True
    
    def generate_next_soup(self) -> bool:
        """Create the BeautifulSoup object and create the hash for the website\n
        If the process is successful return True, otherwise return False"""
        url = Spider.queue[Spider.queue_front]
        Spider.queue_front += 1
        if self.check_if_can_scrape(url) :
            if Spider.try_change_depth() :
                Spider.queue_back = len(Spider.queue)
            html = requests.get(url)
            if html.status_code == 404:
                Spider.unaccessible_urls.append(url)
                return False
            elif html.is_permanent_redirect :
                url = html.url
                if not self.check_if_can_scrape(url):
                    Spider.unaccessible_urls.append(url)
                    return self.check_if_can_scrape(url)
                Spider.queue[Spider.queue_front-1] = url
            self.url = url
            self.soup = BeautifulSoup(html.text, "html.parser")
            self.hash = hashlib.sha256(self.soup.text.encode()).hexdigest()
        else:
            Spider.unaccessible_urls.append(url)
        return self.check_if_can_scrape(url)
    
    def get_text(self) -> str:
        """Get text from website"""
        text = ""
        texts = self.soup.find_all(string = True)
        for i in texts:
            text = f"{text} {i.text.lower()}"
        return text

    #Probably going to change, not the first priority though.
    
    #Try to eliminate the url that leads to a file
    def eliminate_file_url(self, splited_url, to_join):
        if "." in splited_url[-1] and splited_url[-1] != "." and splited_url[-1] != "..":
            splited_url.pop()
            to_join.pop()

    #Translate relative or absolute path into full url
    def parse_url(self, url:str, base_url:str):
        if url[0] == "/": base_url = f"https://{self.get_base_domain(base_url)}"
        splited_url, splited_base = url.split("/"), base_url.split("/")
        to_join = []
        current = -1
        for i in range(len(splited_url)):
            if splited_url[i] == "..":
                while current not in to_join and current > -1: current -= 1
                if current in to_join: to_join.pop()
                elif current == -1 and len(splited_base) > 3: splited_base.pop()
            elif splited_url[i] != "." and splited_url[i] != "":
                to_join.append(i)
                current += 1
        #Try to eliminate the url that leads to a file
        self.eliminate_file_url(splited_url, to_join)
        new_abs_url = ""
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
            if href.startswith("https://") or href.startswith("http://"):
                links.add(href)
            else:
                links.add(self.parse_url(href, self.url))
        return links

    