import json
from pprint import pprint
from time import sleep
from pymongo import MongoClient
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.opera.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


client = MongoClient('localhost', 27017)
db = client['mvideo']
db.drop_collection('mvideo')

options = Options()
options.add_argument('start-maximized')

driver = webdriver.Opera(options=options)
driver.get('https://www.mvideo.ru/')

WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.CLASS_NAME, 'sel-hits-button-next')))
while True:
    button = driver.find_elements_by_class_name('sel-hits-button-next')[2]
    if button.get_attribute('class') == 'next-btn sel-hits-button-next disabled':
        break
    button.click()
    sleep(1)

hits_block = driver.find_elements_by_class_name('sel-hits-block')[1]
gadgets = hits_block.find_elements_by_class_name('gallery-list-item')

for gadget in gadgets:
    product_info = json.loads(gadget.find_element_by_tag_name('a').get_attribute('data-product-info'))
    product_info['_id'] = product_info['productId']
    db.mvideo.insert_one(product_info)

for i in db.mvideo.find({}, {'productCategoryName': 1, 'productVendorName': 1, 'productName': 1,
                             'productPriceLocal': 1, }):
    pprint(i)

driver.close()
