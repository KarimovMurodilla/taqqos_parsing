from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import json
import time
import requests

LINK = 'https://asaxiy.uz'


def browser_init():
    chrome_options = Options()
    chrome_options.set_capability("pageLoadStrategy", "none")
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--window-size=1920,1080')
    browser = webdriver.Chrome(options=chrome_options)

    return browser


def prog(links):
    for link in links:
        browser = browser_init()
        browser.get(link)
        time.sleep(10)
        html = browser.page_source
        soup = BeautifulSoup(html, 'html.parser')

        def ab():
            try:
                items = soup.find(class_='custom-gutter').find_all(class_='product__item')
            except Exception as e:
                print(e)
                items = []
            return items

        try:
            page_count = int(soup.find('ul', class_='pagination').find_all('li')[-2].text)
        except Exception as e:
            print(e)
            page_count = 1

        for ind in range(1, page_count + 1):
            tot_url = link + f'/page={ind}'
            browser.get(tot_url)
            time.sleep(10)

            items = ab()

            print(f'page_count - {page_count}, page - {ind}')
            for item in items:
                item_title = item.find('a', class_='')
                item_url = LINK + item_title.get('href')
                browser.get(item_url)

                time.sleep(10)

                html = browser.page_source
                soup = BeautifulSoup(html, 'html.parser')

                try:
                    product_name = soup.find('h1', class_='product-title').text
                except Exception:
                    continue

                try:
                    img = soup.find('a', class_='swiper-slide item__main-img').get('href')
                except Exception as e:
                    print(e)
                    img = ''

                try:
                    price = ''.join(filter(str.isdigit, soup.find(class_='price-box').find('span',
                                                                                           class_="price-box_new-price").text))
                except Exception as e:
                    print(e)
                    price = '0'

                try:
                    features = soup.find(class_='characteristics').find('table', class_="table").find('tbody').find_all(
                        'tr')
                except Exception:
                    features = ""
                features_list = {}
                if features:
                    for feature in features:
                        try:
                            features_list[feature.find_all('td')[0].text] = feature.find_all('td')[
                                1].text.rstrip().lstrip()
                        except Exception:
                            continue

                try:
                    description = str(soup.find(class_='product__description').find(
                        class_="description__item").text.rstrip().lstrip())
                    if len(description) > 500:
                        description = description[:500]
                except Exception:
                    description = ""

                try:
                    has_credit = True
                    credit_monthly_amount = ''.join(filter(str.isdigit, soup.find(class_="price-box").find(
                        class_="installment__price").text.split('x')[0]))
                except Exception:
                    has_credit = False
                    credit_monthly_amount = ""

                address = " улица Ислама Каримова, 49, Ташкент "
                phone_number = "+998 71 200 01 05 "

                delivery_info = "Заказы, оформленные через сайт Asaxiy.uz, доставляются по Узбекистану."
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
                    'website': 'Asaxiy',
                    'website_link': str(item_url)
                }
                print(product_name)
                requests.post('https://api.taqqoz.uz/v1/product/price/create/', data=obj)
