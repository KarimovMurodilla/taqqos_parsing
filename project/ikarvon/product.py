import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import json
import time

from celery_config import app

LINK = 'https://ikarvon.uz'


def browser_init():
    chrome_options = Options()
    chrome_options.set_capability("pageLoadStrategy", "none")
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--window-size=1920,1080')  
    browser = webdriver.Chrome(options=chrome_options)

    return browser


@app.task
def parse_product(links):
    for link in links:
        print(link)
        browser = browser_init()
        browser.get(link)
        time.sleep(10)
        html = browser.page_source
        soup = BeautifulSoup(html, 'html.parser')

        def ab():
            i = 0
            items = []
            while i < 3:
                try:
                    items = soup.find(class_='products-wrap').find_all(class_='product-item')
                    break
                except Exception as e:
                    print(e)
                    i += 1
                    time.sleep(1)
            return items

        try:
            page_count = int(soup.find('ul', class_='pagination-list').find_all('li')[-1].text)
        except Exception as e:
            print(e)
            page_count = 1

        for ind in range(1, page_count+1):
            tot_url = link+f'?page={ind}'
            browser.get(tot_url)
            time.sleep(5)

            items = ab()

            print(f'page_count - {page_count}, page - {ind}')
            for item in items:
                a = item.find('a')
                item_url = a.get('href')
                browser.get(item_url)

                time.sleep(5)

                html = browser.page_source
                soup = BeautifulSoup(html, 'html.parser')


                try:
                    product_name = soup.find(class_='product-view').find(class_='content-top').find('h1').text
                except Exception as e:
                    print(e)
                    continue

                try:
                    img = soup.find(class_='swiper-wrapper').find('a')['href']
                    img = LINK + str(img)
                except Exception as e:
                    print(e)
                    img = ''

                try:
                    price =''.join(filter(str.isdigit, soup.find(class_='product-about').find('p', class_='text-price').text))
                except Exception:
                    price = '0'

                has_credit = False
                credit_monthly_amount = '0'

                try:
                    features = soup.find(class_='product-characters').find('ul', class_="product-characters__list").find_all('li')
                except Exception:
                    features = ""
                features_list = {}
                if features:
                    for feature in features:
                        try:
                            features_list[feature.find('span').text] = feature.find('strong').text.rstrip().lstrip()
                        except Exception:
                            continue

                try:
                    description = "".join(p.text for p in soup.find(id="product-description").find_all("p"))
                except Exception as e:
                    print(e)
                    description = ""

                address = '100057, Узбекистан, г. Ташкент, Уста Ширин, 136'
                phone_number = "+998 55 503 88 00"
                delivery_info = "Бесплатная доставка по Ташкенту"
                has_delivery = True

                obj = {
                    'name' : str(product_name),
                    'photo' : str(img),
                    'price_amount': str(price),
                    'description' : str(description),
                    'features' : json.dumps(features_list),
                    'has_credit' : has_credit,
                    'credit_monthly_amount' : credit_monthly_amount,
                    'has_delivery': has_delivery,
                    'address': address,
                    'phone_number': phone_number,
                    'delivery_info': delivery_info,
                    'website': 'Ikarvon',
                    'website_link': str(item_url)
                }
                print(f"Ikarvon, {product_name}")
                try:
                    r = requests.post('https://api.taqqoz.uz/v1/product/price/create/', data=obj, timeout=120)
                    print(r.status_code)
                except Exception as e:
                    print(e)
