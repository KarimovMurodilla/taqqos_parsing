from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time
import traceback

from schemas import CategorySchema
from services import create_category

LINK = 'https://elmakon.uz'


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
    browser.get(LINK)
    time.sleep(1)

    try:
        html = browser.page_source
        soup = BeautifulSoup(html, 'html.parser')
        category_list = soup.find(class_='ut2-menu__inbox').find('ul', class_='ty-menu__items').find_all('li', class_='ty-menu__item')
    except Exception:
        traceback.print_exc()
        category_list = [1]

    del category_list[0]

    for cat_item in category_list:
        for sub_cat in cat_item.find(class_='ty-menu__submenu-items').find_all(class_='ty-menu__submenu-item'):
            a = sub_cat.find(class_='ty-menu__submenu-link')
            cat_url = a.get('href')
            cat_name = a.text.strip()
            data = {
                "name": cat_name,
                "url": cat_url,
                "website": "elmakon"
            }
            data = CategorySchema(**data)
            create_category(data=data)
