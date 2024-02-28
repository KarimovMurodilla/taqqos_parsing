from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time


LINK = 'https://maxcom.uz'


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
    i = 0
    category_list = []
    while i < 3:
        try:
            html = browser.page_source
            soup = BeautifulSoup(html, 'html.parser')
            category_list = soup.find(class_='menu__content').find('ul', class_='menu--dropdown').find_all('li')
            break
        except Exception as e:
            print(e)
            i += 1
            time.sleep(1)
    
    for category in category_list:
        a = category.find('a')
        item_url = a.get('href')
        if item_url and item_url != "#":
            item_name = a.text.strip()
            data = {
                'name': item_name,
                'url': item_url,
                'website': 'maxcom'
            }
            print(data)
