from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time

from schemas import CategorySchema
from services import create_category

LINK = 'https://radius.uz'


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
    time.sleep(10)
    button = browser.find_element(By.CLASS_NAME, 'catalog__btn--new')
    browser.execute_script("arguments[0].click();", button)
    navbar = WebDriverWait(browser, 3).until(EC.presence_of_element_located((By.CLASS_NAME, 'catalog__dropdown')))
    while True:
        try:
            html = navbar.get_attribute('outerHTML')
            soup = BeautifulSoup(html, 'html.parser')
            category_list = soup.find('ul', class_='catalog__list').find_all('li', class_='catalog__item')
            break
        except Exception:
            time.sleep(0.5)
    for cat_item in category_list:
        sub_cats = cat_item.find(class_='catalog__box').find_all(class_='catalog__col-group')
        for sub_cat in sub_cats:
            child_sub_cats = sub_cat.find_all(class_='catalog__col-child')
            if child_sub_cats:
                for child_sub_cat in child_sub_cats:
                    a = child_sub_cat.find('a', class_='catalog__col-item')
                    sub_cat_item_url = a.get('href')
                    sub_cut_url = LINK + sub_cat_item_url
                    sub_cat_name = a.text.strip()
                    data = {
                        'name': sub_cat_name,
                        'url': sub_cut_url,
                        'website': 'radius'
                    }
                    data = CategorySchema(**data)
                    create_category(data=data)
            else:
                a = sub_cat.find(class_='catalog__col').find('a', class_='catalog__col-item')
                sub_cat_item_url = a.get('href')
                sub_cut_url = LINK + sub_cat_item_url
                sub_cat_name = a.text.strip()
                data = {
                    'name': sub_cat_name,
                    'url': sub_cut_url,
                    'website': 'radius'
                }
                data = CategorySchema(**data)
                create_category(data=data)
