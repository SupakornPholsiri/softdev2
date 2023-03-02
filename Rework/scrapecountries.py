from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import os
from bs4 import BeautifulSoup
import time  
import pyautogui
options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)
PATH = 'C:\Program Files (x86)\chromedriver.exe'
s=service = Service(executable_path=PATH)

Home = "https://erp.mju.ac.th/acticleDetail.aspx?qid=868"

driver = webdriver.Chrome(options=options,service=s)
driver.maximize_window()

driver.get('https://erp.mju.ac.th/acticleDetail.aspx?qid=868')

elements = driver.find_elements(By.XPATH,"//*[@title]")
Count = 0
ListCountry = []
for element in elements:
    ListCountry.append(element.text)
new = set(ListCountry)
lastlist= []
for i in new:
    lastlist.append(i)
    Count += 1
print(lastlist,Count)

import pickle

with open('listofallcountries.txt', 'wb') as fp:
    pickle.dump(lastlist, fp)