from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common import exceptions as se
from selenium.webdriver.support.ui import WebDriverWait
import time
from selenium.webdriver.support import expected_conditions as EC
from pprint import pprint
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError as dke

def db_add_one_document(doc, collection):
    try:
        collection.insert_one(doc)
        pprint(doc)
        print('Document successfuly added')
    except dke:
        print('Document already exist')

chrome_options = Options()
chrome_options.add_argument("--window-size=1920,1080")
driver = webdriver.Chrome(executable_path='../chromedriver')

driver.get('https://www.mvideo.ru/')

scroll_high_start = 0
scroll_step = 1080


    
while True:
    time.sleep(4)

    try:
        elem = driver.find_element(By.XPATH, "//button[@class='tab-button ng-star-inserted']")
    except se.NoSuchElementException:
        driver.execute_script(f"window.scrollTo({scroll_high_start}, {scroll_high_start + scroll_step})")

    else:
        elem.click()
        break

    scroll_high_start += scroll_step

while True:
    try:
        wait = WebDriverWait(driver, 10)
        button = wait.until(EC.presence_of_element_located((By.XPATH, "//mvid-carousel[@class='carusel ng-star-inserted']//button[@class='btn forward mv-icon-button--primary mv-icon-button--shadow mv-icon-button--medium mv-button mv-icon-button']")))
        button.click()
    except se.ElementClickInterceptedException:
        break
    except se.ElementNotInteractableException:
        break
        
products = driver.find_elements(By.XPATH, "//mvid-carousel[@class='carusel ng-star-inserted']//div[@class='product-mini-card__name ng-star-inserted']//a")

docs = []

for i in products:
    doc = {}
    product_link = i.get_attribute('href')
    product_label = i.text
    doc['product_link'] = product_link
    doc['product_label'] = product_label
    docs.append(doc)

client = MongoClient('127.0.0.1', 27017)
db = client['mvideo']
mvideo_list_collection = db.mvideo

prices = driver.find_elements(By.XPATH, "//mvid-carousel[@class='carusel ng-star-inserted']//span[@class='price__main-value']")

for i, j in enumerate(prices):
    price = j.text.replace(' ', '')
    docs[i].setdefault('price', price)
    db_add_one_document(docs[i], mvideo_list_collection)

driver.close()