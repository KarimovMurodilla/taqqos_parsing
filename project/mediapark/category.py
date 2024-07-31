import time
import traceback

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup

from schemas import CategorySchema
from services import create_category

LINK = 'https://mediapark.uz'


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
    time.sleep(20)
    while True:
        try:
            html = browser.page_source
            soup = BeautifulSoup(html, 'html.parser')
            category_list = soup.find_all(
                'a',
                class_='border border-back rounded-[24px] p-[17px] flex flex-col items-center min-w-[213px] max-w-[213px]'
            )
            break
        except Exception:
            traceback.print_exc()
            time.sleep(0.5)

    for cat_item in category_list:
        cat_url_half = cat_item.get('href')
        cat_url = LINK + cat_url_half

        browser.get(cat_url)

        time.sleep(15)

        while True:
            try:
                elements = browser.find_elements(By.XPATH, '//button[text()="Eщё"]')
                break
            except Exception:
                traceback.print_exc()
                time.sleep(0.5)

        if elements:
            for element in elements:
                browser.execute_script("arguments[0].click()", element)
                time.sleep(1)

        while True:
            try:
                html = browser.page_source
                soup = BeautifulSoup(html, 'html.parser')
                sub_cats = soup.find_all('a', class_='text-[14px] font-[400] text-gray hover:text-blue-primary')
                break
            except Exception:
                traceback.print_exc()
                time.sleep(0.5)

        for sub_cat_item in sub_cats:
            sub_cat_item_url = sub_cat_item.get('href')
            sub_cat_name = sub_cat_item.text.strip()
            data = {
                'name': sub_cat_name,
                'url': LINK + sub_cat_item_url,
                'website': 'mediapark'
            }
            print(data)
            data = CategorySchema(**data)
            create_category(data=data)
