from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
import time  
import pyautogui
options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)
PATH = 'C:\Program Files (x86)\chromedriver.exe'
s=service = Service(executable_path=PATH)

Home = "https://docs.google.com/forms/d/e/1FAIpQLSeXRKvV1R_gBoB0Ll2n7DoYjSUgKN1qLmJzKloFrRuKgEOcyA/viewform?usp=sf_link"

driver = webdriver.Chrome(options=options,service=s)
driver.maximize_window()

driver.get('https://docs.google.com/forms/d/e/1FAIpQLSeXRKvV1R_gBoB0Ll2n7DoYjSUgKN1qLmJzKloFrRuKgEOcyA/viewform?usp=sf_link')

time.sleep(2)
Login = driver.find_element(By.XPATH,'/html/body/div[2]/div/div[2]/div[3]/div[2]/span/span').click()
time.sleep(4)
Username = driver.find_element(By.XPATH,'//*[@id="identifierId"]')
Username.send_keys("math7064test@gmail.com")
Next1 = driver.find_element(By.XPATH,'//*[@id="identifierNext"]/div/button').click()
time.sleep(4)
Password = driver.find_element(By.XPATH,'//*[@id="password"]/div[1]/div/div[1]/input')
time.sleep(1)
Password.send_keys("831411E6")
Next2 = driver.find_element(By.XPATH,'//*[@id="passwordNext"]/div/button').click()
time.sleep(5)

FirstAns = driver.find_element(By.XPATH,'//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input')
FirstAns.send_keys("MesWInDu")
SecondAns = driver.find_element(By.XPATH,'//*[@id="i15"]').click()
# Select(SecondAns)
ThirdAns = driver.find_element(By.XPATH,'//*[@id="i23"]').click()
# Select(ThirdAns)
FourthAns = driver.find_element(By.XPATH,'//*[@id="mG61Hd"]/div[2]/div/div[2]/div[4]/div/div/div[2]/div/div[1]/div/div[1]/input')
FourthAns.send_keys("ไม่รู้")
FifthAns = driver.find_element(By.XPATH,'//*[@id="mG61Hd"]/div[2]/div/div[2]/div[5]/div/div/div[2]/div/div[1]/div[2]/textarea')
FifthAns.send_keys("หล่อ")
Nextpage = driver.find_element(By.XPATH,'//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div[1]/div/span')
Nextpage.click()
time.sleep(3)
Dropdown = driver.find_element(By.XPATH,'//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div[1]')
Dropdown.click()
time.sleep(2)
pyautogui.press('down',presses=2)
pyautogui.press('enter',presses=2)
# time.sleep(2)
# element = driver.find_element(By.XPATH,'/html/body')
# element.send_keys(Keys.ARROW_DOWN,Keys.RETURN);
# ClickDropdown = driver.find_element(By.XPATH,'//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div[1]/div[3]').click()
# option1 = "Never gonna"
# span = driver.find_element(By.CLASS_NAME,'vRMGwf oJeWuf')
# for i in span:
#   try:
#     i.click()
#   except:
#     continue
# ClickDropdown.select_by_visible_text("Never gonna")
# Dropdown.select_by_value("Never gonna")
time.sleep(4)
satisfy = driver.find_element(By.XPATH,'//*[@id="mG61Hd"]/div[2]/div/div[2]/div[4]/div/div/div[2]/div[1]/span/div/label[11]/div[2]/div/div/div[3]/div').click()
send = driver.find_element(By.XPATH,'//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div[1]/div[2]/span').click()