from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time

from schemas import CategorySchema
from services import create_category

LINK = 'https://goodzone.uz'


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
    browser.get(LINK + '/category')
    time.sleep(10)

    try:
        html = browser.page_source
        soup = BeautifulSoup(html, 'html.parser')
        category_list = soup.find(class_='category_accordionWrapper__Ezpwc').find_all(class_='category_categoryItem__HHt5L')
    except Exception:
        category_list = []

    for cat_item in category_list:
        for ul in cat_item.find_all(class_='mantine-Grid-root'):
            for sub_cat in ul.find_all(class_='mantine-Grid-col'):
                a = sub_cat.find('a')
                cat_url = a.get('href')
                cat_name = a.text.strip()
                data = {
                    "name": cat_name,
                    "url": LINK + cat_url,
                    "website": "goodzone"
                }
                data = CategorySchema(**data)
                print(data)
                create_category(data=data)

