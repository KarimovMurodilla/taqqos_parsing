from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import json
import time
import requests

LINK = 'https://openshop.uz'


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
        print(link)
        browser = browser_init()
        browser.get(link)
        time.sleep(10)
        html = browser.page_source
        soup = BeautifulSoup(html, 'html.parser')

        def ab():
            try:
                items = soup.find(class_='main-content').find(class_='product-wrapper').find_all(
                    class_='product-wrap')
            except Exception as e:
                print(e)
                items = []

            return items

        try:
            page_count = int(
                soup.find(class_='toolbox-pagination').find('ul', class_='pagination').find_all('li', 'page-item')[
                    -1].text)
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
                item_title = item.find(class_='product-details').find('h3', class_='product-name').find('a')
                item_url = item_title.get('href')
                browser.get(item_url)

                time.sleep(10)

                html = browser.page_source
                soup = BeautifulSoup(html, 'html.parser')

                try:
                    product_name = soup.find('h1', class_='product-title').text
                except Exception:
                    continue

                try:
                    img = soup.find('figure', class_='product-image').find('img')['src']
                except Exception as e:
                    print(e)
                    img = ''

                try:
                    price = ''.join(
                        filter(str.isdigit, soup.find(class_='product-price').find('ins', class_="new-price").text))
                except Exception:
                    price = '0'

                try:
                    has_credit = True
                    credit_monthly_amount = ''.join(
                        filter(str.isdigit, soup.find(class_='product-price').find('div').text))
                except Exception:
                    has_credit = False
                    credit_monthly_amount = '0'

                try:
                    features = soup.find(id="product-tab-attributes").find('table', class_='table').find(
                        'tbody').find_all('tr', class_='row')
                except Exception:
                    features = ""
                features_list = {}
                if features:
                    for feature in features:
                        try:
                            features_list[feature.find_all('td')[0].text] = feature.find_all('td')[1].text.rstrip().lstrip()
                        except Exception:
                            continue

                address = "O'zbekiston Respublikasi, Toshkent shahri, Mirzo-Ulug'bek tumani, Buyuk Ipak Yoʻli koʻchasi, 302"
                phone_number = "+998 (71) 200 66 60"
                delivery_info = "O'zbekiston bo'ylab yetkazib berish xizmati"
                description = ""
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
                    'website': 'Openshop',
                    'website_link': str(item_url)
                }
                print(product_name)
                requests.post('https://api.taqqoz.uz/v1/product/price/create/', data=obj)
