from time import sleep
from pymongo import MongoClient
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.opera.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


client = MongoClient('localhost', 27017)
db = client['mails']

options = Options()
options.add_argument('start-maximized')

driver = webdriver.Opera(options=options)
driver.get('https://account.mail.ru/login/')

login = WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.NAME, 'username')))
login.send_keys('study.ai_172@mail.ru')
login.send_keys(Keys.RETURN)

password = WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.NAME, 'password')))
password.send_keys('NextPassword172')
password.send_keys(Keys.RETURN)

# Ждем загрузку списка
WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.CLASS_NAME, 'js-letter-list-item')))

# Убираем группировку писем
button = driver.find_element_by_class_name('settings')
button.click()
sleep(1)
try:
    group = driver.find_element_by_class_name('checkbox__box_checked')
    group.click()
except:
    print('Группировка уже выключена')
sleep(1)

links, last_mail = [], 0

while True:
    mails = driver.find_elements_by_class_name('js-letter-list-item')

    if mails[-1] == last_mail:
        break
    else:
        last_mail = mails[-1]

    for mail in mails:
        link = mail.get_attribute('href')
        links.append(link)
    actions = ActionChains(driver)
    actions.move_to_element(last_mail)
    actions.perform()

for link in links:
    driver.get(link)
    subject = WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.CLASS_NAME, 'thread__subject')))
    author = driver.find_element_by_class_name('letter-contact')
    date = driver.find_element_by_class_name('letter__date')
    text = driver.find_element_by_class_name('letter__body')
    db.mail_ru.insert_one({'author': author.text, 'date': date.text, 'subject': subject.text, 'text': text.text})

driver.close()
