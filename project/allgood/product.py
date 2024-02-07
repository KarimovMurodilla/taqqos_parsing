from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import json
import time
import requests

LINK = 'https://allgood.uz'


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
            items = []
            try:
                items = soup.find('article', class_='catalog-content').find(class_='products-wrap').find_all(
                    class_='product-card__parent')
            except Exception as e:
                print(e)
            return items

        try:
            page_count = int(soup.find('ul', class_='pagination-list').find_all('li')[-1].text)
        except Exception as e:
            print(e)
            page_count = 1

        for ind in range(1, page_count + 1):
            tot_url = link + f'?page={ind}'
            browser.get(tot_url)
            time.sleep(10)

            items = ab()

            print(f'page_count - {page_count}, page - {ind}')
            for item in items:
                item_title = item.find(class_='product-card__content').find(class_='product-card__body').find('a')
                item_url = item_title.get('href')
                browser.get(item_url)

                time.sleep(10)

                html = browser.page_source
                soup = BeautifulSoup(html, 'html.parser')

                try:
                    product_name = soup.find('section', class_='product-view').find('h1').text
                except Exception:
                    continue

                try:
                    img = soup.find(class_='product-preview__swiper').find('img', class_='img-fluid')['src']
                    img = LINK + str(img)
                except Exception as e:
                    print(e)
                    img = ''

                try:
                    price = ''.join(
                        filter(str.isdigit, soup.find(class_='product-about').find('p', class_="text-price").text))
                except Exception:
                    price = '0'

                try:
                    has_credit = True
                    credit_monthly_amount = ''.join(filter(str.isdigit,
                                                           soup.find(class_='partner-installments-list').find('span',
                                                                                                              class_='partner-installment-price').text))
                except Exception:
                    has_credit = False
                    credit_monthly_amount = '0'

                try:
                    features = soup.find(class_="product-character").find('ul',
                                                                          class_='product-character__list').find_all(
                        'li')
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
                    description = soup.find(id="product-description").find('div', class_='open').text
                except Exception:
                    description = ""

                address = ""
                phone_number = "+998 55 520-90-90"
                delivery_info = ""
                has_delivery = False

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
                    'website': 'Allgood',
                    'website_link': str(item_url)
                }
                print(product_name)
                requests.post('https://api.taqqoz.uz/v1/product/price/create/', data=obj)