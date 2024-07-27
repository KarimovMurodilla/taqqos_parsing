import logging

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time

from schemas import CategorySchema
from services import create_category

LINK = 'https://texnomart.uz'


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
    browser.get(LINK+'/ru/')
    time.sleep(5)

    while True:
        try:
            html = browser.page_source
            soup = BeautifulSoup(html, 'html.parser')
            category_list = soup.find(class_='catalog-dropdown').find(class_='catalog-right').find_all('aside')
            break
        except Exception as e:
            logging.warning(e)
            time.sleep(0.5)
    for cat_item in category_list:
        for sub_cat in cat_item.find_all('ul'):
            for item in sub_cat:
                for a in item.find_all('a', class_="catalog-last"):
                    cat_url_half = a.get('href')
                    cat_url = LINK + cat_url_half
                    cat_name = a.text.strip()
                    data = {
                        "name": cat_name,
                        "url": cat_url,
                        "website": "texnomart"
                    }
                    print(data)
                    data = CategorySchema(**data)
                    create_category(data=data)
