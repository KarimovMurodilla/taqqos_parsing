from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time

from schemas import CategorySchema
from services import create_category

LINK = 'https://asaxiy.uz'


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
    time.sleep(5)
    button = browser.find_element(By.CLASS_NAME, 'open__menu')
    button.click()
    navbar = WebDriverWait(browser, 1).until(EC.presence_of_element_located((By.CLASS_NAME, 'mega__menu')))
    try:
        html = navbar.get_attribute('outerHTML')
        soup = BeautifulSoup(html, 'html.parser')
        category_list = soup.find(class_='mega__menu-left').find('ul', class_='mega__menu-list').find_all('li')
    except Exception as e:
        print(e)
        category_list = []

    for cat_item in category_list:
        a = cat_item.find('a')
        cat_item_url = a.get('href')
        cat_url = LINK + cat_item_url
        browser.get(cat_url)

        time.sleep(10)
        try:
            html = browser.page_source
            soup = BeautifulSoup(html, 'html.parser')
            sub_cats = soup.find('ul', id='category_list').find_all('li')
        except Exception as e:
            print(e)
            time.sleep(0.5)

        if sub_cats:
            for sub_cat in sub_cats:
                a = sub_cat.find('a')
                sub_cat_item_url = a.get('href')
                sub_cut_url = LINK + sub_cat_item_url
                sub_cat_name = a.text.strip()
                data = {
                    'name': sub_cat_name,
                    'url': sub_cut_url,
                    'website': 'asaxiy'
                }
                data = CategorySchema(**data)
                create_category(data=data)
        else:
            data = {
                'name': a.text.strip(),
                'url': cat_url,
                'website': 'asaxiy'
            }
            data = CategorySchema(**data)
            create_category(data=data)
