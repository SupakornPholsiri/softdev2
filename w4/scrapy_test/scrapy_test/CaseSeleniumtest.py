from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time  
import requests
from bs4 import BeautifulSoup
from pythainlp import word_tokenize
import csv
import re

options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)
PATH = 'C:\Program Files (x86)\chromedriver.exe'
s=service = Service(executable_path=PATH)

driver = webdriver.Chrome(options=options,service=s)
driver.maximize_window()
driver.get("https://www.thairath.co.th/home")


class SeleniumInteract():
    def __init__(self,url):
        self.driver = webdriver.Chrome(options=options,service=s)
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        options = webdriver.ChromeOptions()
        options.add_experimental_option("detach", True)
        PATH = 'C:\Program Files (x86)\chromedriver.exe'
        service = Service(executable_path=PATH)
        self.driver = webdriver.Chrome(options=options,service=service)
        self.url = url
        
    def crawler(self,url):
        #ไล่รันฟังก์ชั่นสำหรับเเต่ละประเภท element
        self.driver.get(self.url)
        self.navbarinteract()
            
    
    def navbarinteract(self,by=By):
        #หา Element ที่มีคำว่า nav
        container = driver.find_elements(by.XPATH,".//*[contains(@id,'nav')]")
        for nav in range(len(container)):
            #Do Try to find href in navbar
            try:
                url = container[nav].get_attribute('href')
                #case whe url don't have base url
                if not url.startswith("http") :
                    url = self.url + url
                #check HTML Parser
                driver.get(url)                         #ช่วงนี้อาจะเพิ่ม Depth ในอนาคต
                source = driver.page_source
                soup = BeautifulSoup(source,"html.parser")
                print(soup.prettify())
            except:
                continue
   