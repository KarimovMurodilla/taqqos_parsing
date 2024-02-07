from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time

from schemas import CategorySchema
from services import create_category

LINK = 'https://allgood.uz'


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
    browser.get(LINK + '/categories')
    time.sleep(5)
    while True:
        try:
            html = browser.page_source
            soup = BeautifulSoup(html, 'html.parser')
            category_list = soup.find_all('a', class_='sub-categories-box')
            break
        except Exception:
            time.sleep(0.5)

    for cat_item in category_list:
        cat_url = cat_item.get('href')

        browser.get(cat_url)

        time.sleep(5)

        while True:
            try:
                html = browser.page_source
                soup = BeautifulSoup(html, 'html.parser')
                sub_cats = soup.find('ul', class_='navbar-d__list').find_all('li', class_='navbar-d__item')
                break
            except Exception:
                time.sleep(0.5)

        for sub_cat_item in sub_cats:
            a = sub_cat_item.find('a', class_='navbar-d__link')
            sub_cat_item_url = a.get('href')
            sub_cat_name = a.text.strip()
            data = {
                'name': sub_cat_name,
                'url': sub_cat_item_url,
                'website': 'allgood'
            }
            data = CategorySchema(**data)
            create_category(data=data)

