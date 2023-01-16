import requests
from bs4 import BeautifulSoup
from pythainlp import word_tokenize
import csv
import re
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time  
from pymongo import MongoClient
client = MongoClient('localhost:27017')
SearchEngine = client['SearchEngine']
dbweb = SearchEngine['WebDB']
from collections import Counter

class Index:
    #Class for indexes. Methods related to index are stored here.
    def __init__(self):
        self.index = {}

    #Add or add onto keyword index using the tokens.
    def modify_index_with_tokens(self, tokens, url):
        #Pattern for removing most punctuations and special characters tokens
        pattern = re.compile(r'[\n/,.\[\]()_:;/?! ‘\xa0©=“”{}%_&<>’\|"]')
        counter = Counter(token)
        for token in tokens:
            #Remove None, punctuations and special characters tokens
            if not token or pattern.match(token):
                continue
            if token not in self.index.values()  :
                self.index[token] = {url:counter[token]}
                dbweb.insert_one({"key":token,"value":self.index[token]})
            elif url not in self.index.values():
                self.index[token][url] = str(counter[token])
                dbweb.find_one_and_update({"key":token},{'$set':{"value":self.index["value"]}})
            elif url in self.index.values() and self.index.values()[url] != counter[token]:
                self.index[token][url] = str(counter[token])
                dbweb.find_one_and_update({"key":token},{'$set':{"value":self.index["value"]}})
        return self.index
    #Save current index to csv file
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
    #The web crawler
    queue = []
    crawled = []
    
    #Create the spider with seed url as starting point
    def __init__(self, url, depth = None):
        self.depth = depth
        self.url = url
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
        self.generate_soup(link)
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
            """print("*")
            print(href)"""
            if href.startswith("https://") or href.startswith("http://") :
                if self.get_base_domain(href) == self.base_domain:
                    links.add(href)
            else:
                links.add(self.parse_url(href, self.url))
        return links

if __name__ == "__main__":
    spider = Spider("https://iot-kmutnb.github.io/blogs")
    index = Index()
    print(Spider.queue, end = "\n------------------------------------------\n")
    print(Spider.crawled)
    while len(Spider.queue) > 0:
        index.modify_index_with_tokens(word_tokenize(spider.crawl(Spider.queue.pop())), spider.url)
        print("URL in queue:", len(Spider.queue),"|","URL in crawled:", len(Spider.crawled), f"Scraped {spider.url}")
    index.save_to_file()