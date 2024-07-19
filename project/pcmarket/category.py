from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time

from celery_config import app
from schemas import CategorySchema
from services import create_category

LINK = 'https://pcmarket.uz'


def browser_init():
    chrome_options = Options()
    chrome_options.set_capability("pageLoadStrategy", "none")
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--window-size=1920,1080')
    browser = webdriver.Chrome(options=chrome_options)
    return browser


# @app.task
def parse_category():
    browser = browser_init()
    browser.get(LINK)
    time.sleep(10)
    i = 0
    category_list = []
    while i < 3:
        try:
            html = browser.page_source
            soup = BeautifulSoup(html, 'html.parser')
            category_list = soup.find(id='nav_menu-2').find('ul', id='menu-bokovoe-menju').find_all('li', class_='menu-item')
            break
        except Exception as e:
            print(e)
            i += 1
            time.sleep(1)

    for category in category_list:
        try:
            sub_menu = category.find('ul', class_='sub-menu').find_all('li', class_='menu-item')
        except Exception:
            sub_menu = []
        if sub_menu:
            for li in sub_menu:
                a = li.find('a')
                item_url = a.get('href')
                item_name = a.text.strip()
                data = {
                    'name': item_name,
                    'url': item_url,
                    'website': 'pcmarket'
                }
                data = CategorySchema(**data)
                create_category(data=data)
        else:
            a = category.find('a')
            item_url = a.get('href')
            item_name = a.text.strip()
            data = {
                'name': item_name,
                'url': item_url,
                'website': 'pcmarket'
            }
            data = CategorySchema(**data)
            create_category(data=data)
