from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time

from schemas import CategorySchema
from services import create_category

LINK = 'https://openshop.uz'


def browser_init():
    chrome_options = Options()
    chrome_options.set_capability("pageLoadStrategy", "none")
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--window-size=1920,1080')
    browser = webdriver.Chrome(options=chrome_options)
    return browser


def prog():
    browser = browser_init()
    browser.get(LINK + '/shop/categories')
    time.sleep(10)

    while True:
        try:
            html = browser.page_source
            soup = BeautifulSoup(html, 'html.parser')
            category_list = soup.find_all(class_='sub-category-menu')
            break
        except Exception:
            time.sleep(0.5)

    for cat_item in category_list:
        for ul in cat_item.find_all('ul', class_='row'):
            for sub_cat in ul.find_all('li'):
                a = sub_cat.find('a')
                cat_url = a.get('href')
                cat_name = a.text.strip()
                data = {
                    "name": cat_name,
                    "url": cat_url,
                    "website": "openshop"
                }
                data = CategorySchema(**data)
                create_category(data=data)
