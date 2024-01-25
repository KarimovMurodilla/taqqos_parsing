from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time

from selenium.webdriver.chrome.service import Service
from sqlalchemy.orm import Session
from webdriver_manager.chrome import ChromeDriverManager

from db.get_db import database_connect
from models.texnomart import Category
from schemas import CategorySchema

LINK = 'https://texnomart.uz'


@database_connect
def create_category(db: Session, data: CategorySchema) -> None:
    category = db.query(Category).filter(Category.name == data.name).first()
    if category is None:
        category = Category(**data.dict())
        db.add(category)
    else:
        category.name = data.name
    db.commit()


def get_all_categories(db: Session):
    categories = db.query(Category)
    return categories


def browser_init():
    chrome_options = Options()
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-dev-shm-usage')
    browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    return browser


def prog():
    browser = browser_init()
    browser.get(LINK+'/ru/')
    time.sleep(1)

    while True:
        try:
            html = browser.page_source
            soup = BeautifulSoup(html, 'html.parser')
            category_list = soup.find(class_='catalog-dropdown').find(class_='catalog-right').find_all('aside')
            break
        except:
            time.sleep(0.5)
    for cat_item in category_list:
        for sub_cat in cat_item.find_all('ul'):
            for item in sub_cat:
                for a in item.find_all('a', class_="catalog-last"):
                    cat_url_half = a.get('href')
                    cat_url = LINK + cat_url_half
                    cat_name = a.text.strip()
                    data = {
                        "name": cat_name,
                        "url": cat_url,
                    }
                    create_category(data=data)
