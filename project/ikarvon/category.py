from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time
from celery_config import app

from schemas import CategorySchema
from services import create_category

LINK = 'https://ikarvon.uz/'


def browser_init():
    chrome_options = Options()
    chrome_options.set_capability("pageLoadStrategy", "none")
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--window-size=1920,1080')
    chrome_options.add_argument('--disable-dev-shm-usage')

    browser = webdriver.Chrome(options=chrome_options)
    return browser


@app.task
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
            category_list = soup.find(class_='catalog-menu-d').find(class_='catalog-menu-d__wrap').find_all(class_='catalog-menu-d__content-container')
            break
        except Exception as e:
            print(e)
            i += 1
            time.sleep(1)
    for category in category_list:
        for li in category.find_all(class_='catalog-menu-d-nav'):
            a = li.find('a')
            item_url = a.get('href')
            item_name = a.text.strip()
            data = {
                'name': item_name,
                'url': item_url,
                'website': 'ikarvon'
            }
            data = CategorySchema(**data)
            create_category(data=data)
