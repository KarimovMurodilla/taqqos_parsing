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
    chrome_options.set_capability("pageLoadStrategy", "normal")  # Try 'normal' or 'eager' instead of 'none'
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--window-size=1920,1080')
    chrome_options.add_argument('--remote-debugging-port=9222')  # Useful for debugging
    chrome_options.add_argument('--enable-logging')
    chrome_options.add_argument('--v=1')
    browser = webdriver.Chrome(options=chrome_options)
    return browser


def prog():
    browser = browser_init()
    browser.get(LINK + '/category')
    time.sleep(5)
    print("After time sleep 1")
    while True:
        try:
            html = browser.page_source
            soup = BeautifulSoup(html, 'html.parser')
            category_list = soup.find_all(
                'a',
                class_='border border-back rounded-[24px] p-[17px] flex flex-col items-center min-w-[213px] max-w-[213px]'
            )
            print("Inside while 1")
            break
        except Exception:
            traceback.print_exc()
            time.sleep(0.5)

    print("Before for 1")
    print("Category_list", category_list)
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
                print("Sub cats:", sub_cats)
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
