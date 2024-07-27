from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import json
import time
import requests

LINK = 'https://radius.uz'


def browser_init():
    chrome_options = Options()
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--window-size=1920,1080')
    chrome_options.set_capability("pageLoadStrategy", "none")
    browser = webdriver.Chrome(options=chrome_options)

    return browser


def prog(links):
    for link in links:
        browser = browser_init()
        browser.get(link)
        time.sleep(20)
        html = browser.page_source
        soup = BeautifulSoup(html, 'html.parser')

        def ab():

            try:
                items = soup.find(class_='grid').find_all(class_='grid__item')
            except Exception as e:
                print(e)
                items = []
            return items

        try:
            page_count = int(
                soup.find('ul', class_='pagination__list').find_all('li', class_='pagination__numb')[-1].text)
        except Exception as e:
            print(e)
            page_count = 1

        for ind in range(1, page_count + 1):
            tot_url = link + f'?page={ind}'
            browser.get(tot_url)
            time.sleep(20)

            items = ab()

            print(f'page_count - {page_count}, page - {ind}')
            for item in items:
                item_title = item.find('a', class_='card__photo')
                item_url = LINK + item_title.get('href')
                browser.get(item_url)

                time.sleep(10)

                html = browser.page_source
                soup = BeautifulSoup(html, 'html.parser')

                try:
                    product_name = soup.find('p', class_='product__title').text
                except Exception:
                    continue

                try:
                    img = soup.find('span', class_='product__photo').get('data-src')
                except Exception as e:
                    print(e)
                    img = ''

                try:
                    price = ''.join(filter(str.isdigit, soup.find(class_='product__main--right').find('h3',
                                                                                                      class_="product__main--price").text))
                except Exception as e:
                    print(e)
                    price = '0'

                try:
                    features = soup.find('table', class_="char").find('tbody').find_all('tr')
                except Exception as e:
                    print(e)
                    features = ""
                features_list = {}
                if features:
                    for feature in features:
                        try:
                            features_list[feature.find('td', class_='char__type').text] = feature.find('td',
                                                                                                       class_='char__val').text.rstrip().lstrip()
                        except Exception:
                            continue

                try:
                    description = str(soup.find(class_='tab__body').find(class_="description").text.rstrip().lstrip())
                    if len(description) > 1000:
                        description = description[:1000]
                except Exception:
                    description = ""

                try:
                    has_credit = True
                    credit_monthly_amount = ''.join(filter(str.isdigit,
                                                           soup.find(class_="product__main--right").find_all(
                                                               class_="product__main--text-blue")[-1].text))
                except Exception as e:
                    print(e)
                    has_credit = False
                    credit_monthly_amount = ""

                address = "Шота Руставели 150, 100121, Tashkent, Toshkent Shahri, Uzbekistan"
                phone_number = "+998 71 200 31 00"

                delivery_info = "Курьером (пн-пт). Курьер доставит товар в день заказа с 18 до 22.00 (при условии, что заказ сформирован до 16.00), либо вечером следующего дня (если заказ сформирован после 16.00)."
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
                    'website': 'Radius',
                    'website_link': str(item_url)
                }
                print(product_name)
                requests.post('https://api.taqqoz.uz/v1/product/price/create/', data=obj)
