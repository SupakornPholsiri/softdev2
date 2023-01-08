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

class SeleniumInteract():
    def __init__(self):
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        options.add_experimental_option("detach", True)
        PATH = 'C:\Program Files (x86)\chromedriver.exe'
        service = Service(executable_path=PATH)
        self.driver = webdriver.Chrome(options=options,service=service)
        
    def crawler(self,url):
        #ไล่รันฟังก์ชั่นสำหรับเเต่ละประเภท element
        self.driver.get(url)
        self.navbarinteract()
    
    def navbarinteract(self,by=By):
        #ฟังชั่นก์ Scrape ประเภท Navbar
        # container = self.driver.find_elements(by.XPATH,'//*[@id="Navbar" OR @id = "navbar"]')
        # aaa = container.__class__
        # for nav in range(container):
        #     self.driver.find_element(by.XPATH,'//')
        #     container[nav].click()
        container = self.driver.find_elements(by.XPATH,".//*[contains(@id,'Navbar')]")
        for nav in range(len(container)):
            try:
                url = container[nav].get_attribute('href')
                self.driver.get(url)                         #ช่วงนี้อาจะเพิ่ม Depth ในอนาคต
                source = self.driver.page_source
                soup = BeautifulSoup(source,"html.parser")
                print(soup.prettify())
            except:
                continue
   