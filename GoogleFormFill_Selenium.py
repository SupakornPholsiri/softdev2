from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
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

driver.implicitly_wait(10)
Login = driver.find_element(By.XPATH,'/html/body/div[2]/div/div[2]/div[3]/div[2]/span/span').click()
driver.implicitly_wait(10)
Username = driver.find_element(By.XPATH,'//*[@id="identifierId"]')
Username.send_keys("supakornkmutnb@gmail.com")
Next1 = driver.find_element(By.XPATH,'//*[@id="identifierNext"]/div/button').click()
driver.implicitly_wait(10)
Password = driver.find_element(By.XPATH,'//*[@id="password"]/div[1]/div/div[1]/input')
driver.implicitly_wait(10)
Password.send_keys("nung2003")
Next2 = driver.find_element(By.XPATH,'//*[@id="passwordNext"]/div/button').click()
driver.implicitly_wait(10)
time.sleep(10)

def fill_text(element, ans):
    element.find_element(By.XPATH, './/input[@type="text"]').send_keys(ans)
    time.sleep(1)

def fill_radio_button(element, ans):
    element.find_element(By.XPATH, f'.//div[@data-value="{ans}"]').click()

def fill_multiple_choice(element, answers):
    for ans in answers:
        element.find_element(By.XPATH, f'.//div[@data-answer-value="{ans}"]').click()

def fill_paragraph(element, ans):
    element.find_element(By.XPATH, './/textarea').send_keys(ans)
    time.sleep(1)

def fill_dropdown(element, ans):
    dropdown = element.find_element(By.XPATH, './/div[@role="listbox"]')
    dropdown.click()
    time.sleep(2)
    choices = dropdown.find_elements(By.XPATH, './/span[@class="vRMGwf oJeWuf"]')
    count = 0
    for i in range(int(len(choices)/2), len(choices)):
        if ans == choices[i].text:
            break
        count += 1
    time.sleep(1)
    for i in range(count):
        pyautogui.press('down')
    pyautogui.press('enter')

def fill_date(element, ans):
    element.find_element(By.XPATH, './/input[@type="date"]').send_keys(ans)

def fill_linear_scale(element, ans):
    element.find_element(By.XPATH, f'.//div[@data-value={ans}]').click()

def fill_form(ans1, ans2, ans3, ans4, ans5, ans6, ans7, ans8, ans9):

    listItems = [item for item in driver.find_elements(By.XPATH, '//div[@class="Qr7Oae" and @role="listitem"]')]

    Q1 = listItems[0]
    fill_text(Q1, ans1)

    Q2 = listItems[1]
    fill_radio_button(Q2, ans2)

    Q3 = listItems[2]
    fill_multiple_choice(Q3, ans3)

    Q4 = listItems[3]
    fill_text(Q4, ans4)

    Q5 = listItems[4]
    fill_paragraph(Q5, ans5)

    Nextpage = driver.find_element(By.XPATH,'//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div[1]/div/span')
    Nextpage.click()
    driver.implicitly_wait(10)

    listItems2 = [item for item in driver.find_elements(By.XPATH, '//div[@class="Qr7Oae" and @role="listitem"]')]

    Q6 = listItems2[2]
    fill_dropdown(Q6, ans6)

    Q7 = listItems2[3]
    fill_dropdown(Q7, ans7)

    Q8 = listItems2[4]
    fill_date(Q8, ans8)

    Q9 = listItems2[5]
    fill_linear_scale(Q9, ans9)

    time.sleep(2)
    driver.find_element(By.XPATH,'//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div[1]/div[2]/span').click()

fill_form("Nung", "ไม่ตอบ", ["นกพิราบเป็นกล้องวงจรปิดของรัฐบาล", "Python เป็นภาษาพูด"], "0", "ไม่มี", "Give you up", "Another test", "12302015", 10)