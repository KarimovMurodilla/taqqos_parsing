import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import json
import time
import re

from celery_config import app

LINK = 'https://pcmarket.uz'


def browser_init():
    chrome_options = Options()
    chrome_options.set_capability("pageLoadStrategy", "none")
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--window-size=1920,1080')
    chrome_options.add_argument('--disable-dev-shm-usage')
    
    browser = webdriver.Chrome(options=chrome_options)

    return browser


# @app.task
def parse_product(links):
    for link in links:
        print(link)
        browser = browser_init()
        browser.get(link)
        time.sleep(10)
        html = browser.page_source
        soup = BeautifulSoup(html, 'html.parser')

        def ab(browser):
            i = 0
            items = []
            html = browser.page_source
            soup = BeautifulSoup(html, 'html.parser')
            while i < 3:
                try:
                    items = soup.find('ul', class_='products').find_all('li', class_='product')
                    break
                except Exception as e:
                    print(e, "SSSSSS")
                    i += 1
                    time.sleep(1)
            return items

        try:
            page_count = int(soup.find('ul', class_='page-numbers').find_all('li')[-2].text)
        except Exception as e:
            print(e)
            page_count = 1

        for ind in range(1, page_count+1):
            tot_url = link+f'/page/{ind}'
            browser.get(tot_url)
            time.sleep(5)

            items = ab(browser)

            print(f'page_count - {page_count}, page - {ind}')
            for item in items:
                a = item.find('a')
                item_url = a.get('href')
                browser.get(item_url)

                time.sleep(5)

                html = browser.page_source
                soup = BeautifulSoup(html, 'html.parser')


                try:
                    product_name = soup.find(class_='summary entry-summary').find('h2').text
                except Exception as e:
                    print(e)
                    continue

                try:
                    img = soup.find(class_='woocommerce-product-gallery__image').find('a')['href']
                except Exception as e:
                    print(e)
                    img = ''

                try:
                    price =''.join(filter(str.isdigit, soup.find('span', class_='woocommerce-Price-amount amount').find('bdi').text))
                except Exception:
                    price = '0'

                has_credit = False
                credit_monthly_amount = '0'

                try:
                    features = soup.find(class_="summary entry-summary").find("ul", class_='char-list').find_all('li')
                except Exception as e:
                    print(e)
                    features = ""
                features_list = {}
                if features:
                    for feature in features:
                        try:
                            text = feature.text
                            key = " ".join(word for word in text.split() if bool(re.search('[а-яА-Я]', word)))
                            val = text.lstrip(key)
                            features_list[key] = val
                        except Exception as e:
                            print(e)
                            continue

                try:
                    description = "".join(p.text for p in soup.find(id="tab-description").find_all("p"))
                except Exception as e:
                    print(e)
                    description = ""

                address = 'Узбекистан, Ташкент, Юнусабадский район, 13-й квартал, 2А, Торговый Комплекс "Lion" Ориентир "Mega Planet".'
                phone_number = "+99899 301-31-00"
                delivery_info = "ДОСТАВИМ БЕСПЛАТНО ПО ТАШКЕНТУ ДОСТАВКА В РЕГИОНЫ УЗБЕКИСТАНА"
                has_delivery = True

                obj = {
                    'name': str(product_name),
                    'photo': str(img),
                    'price_amount': str(price),
                    'description': str(description),
                    'features': json.dumps(features_list),
                    'has_credit': has_credit,
                    'credit_monthly_amount': credit_monthly_amount,
                    'has_delivery': has_delivery,
                    'address': address,
                    'phone_number': phone_number,
                    'delivery_info': delivery_info,
                    'website': 'Pcmarket',
                    'website_link': str(item_url)
                }
                print(f"PCmarket, {product_name}")
                try:
                    r = requests.post('https://api.taqqoz.uz/v1/product/price/create/', data=obj, timeout=120)
                    print(r.status_code)
                except Exception as e:
                    print(e)
