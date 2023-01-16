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
from pymongo import MongoClient
from pymongo import MongoClient
client = MongoClient('localhost:27017')
SearchEngine = client['SearchEngine']
dbweb = SearchEngine['WebDB']

options = webdriver.ChromeOptions()
# options.add_argument('--headless')
# options.add_argument('--disable-gpu')
options.add_experimental_option("detach", True)
PATH = 'C:\Program Files (x86)\chromedriver.exe'
s=service = Service(executable_path=PATH)

Home = "https://www.scrapethissite.com/pages/forms"

driver = webdriver.Chrome(options=options,service=s)
driver.maximize_window()
driver.get(Home)
container = driver.find_elements(By.XPATH,".//*[contains(@class,'nav')]")
# container2 = driver.find_elements(By.XPATH,"//*[@class='pagination']/child::li")

# for nav in range(len(container2)):
#      try:
#          print(container2[nav].text)
#          url = str(container2[nav].get_attribute('href'))
#          print(url)
#          print("https://www.scrapethissite.com/"+url)
#          a = driver.get("https://www.scrapethissite.com/"+url)
#          print(a)
#          source = driver.page_source
#          soup = BeautifulSoup(source,"html.parser")
#         #  print(soup.prettify())
#      except:
#          continue
# ของเเหนบบาร์เเต่ยังไม่ได้เพิ่มลูปข้างในหลังจากเข้าไป
for nav in range(len(container)):
    try:
        url = container[nav].get_attribute('href')
        if not url.startswith("http") :
            url = Home + url
        else:
            driver.get(Home+url)
            sub_container = driver.find_elements(By.TAG_NAME,'a')
            count = 0
            driver.get(Home)    
            source = driver.page_source
            soup = BeautifulSoup(source,"html.parser")
            dbweb.insert_one({"id":1,"user_name":soup.text})
    except:
        continue
   
   



    
