from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import json
import time
import threading
import requests
from webdriver_manager.chrome import ChromeDriverManager

LINK = 'https://texnomart.uz'


def browser_init():
    chrome_options = Options()
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-dev-shm-usage')
    browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    return browser


def get_json_data():
    with open('result.json', 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data


def set_json_data(data):
    with open('result.json', 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False)


main_result = {}


def prog(links, index, step):
    global main_result
    for i in range(index, len(links), step):
        link_data = links[i]
        link = link_data[0]
        link_name = link_data[1]
        browser = browser_init()
        browser.get(link)
        time.sleep(1)

        def ab():

            is_page_loading = True

            while is_page_loading:
                html = browser.page_source
                soup = BeautifulSoup(html, 'html.parser')
                try:
                    items = soup.find(class_='products-box').find_all(class_='product-item-wrapper')
                    is_page_loading = False
                    break
                except Exception:
                    time.sleep(1)
            return items

        items = ab()

        try:
            page_count = int(
                browser.find_element(By.CLASS_NAME, 'pagination').find_elements(By.TAG_NAME, 'span')[-2].text)
        except Exception:
            page_count = 1

        for ind in range(1, page_count + 1):
            tot_url = link + f'?page={ind}'
            browser.get(tot_url)

            items = ab()

            print(f'page_count - {page_count}')
            for item in items:
                item_title = item.find(class_='product-top')
                item_url_half = item_title.find('a').get('href')
                item_url = LINK + item_url_half
                browser.get(item_url)

                time.sleep(10)

                html = browser.page_source
                soup = BeautifulSoup(html, 'html.parser')

                try:
                    product_name = soup.find('h1', class_='product__name').text
                except Exception:
                    continue

                try:
                    img = browser.find_element(By.CLASS_NAME, 'gallery-top__item').find_element(By.TAG_NAME,
                                                                                                'img').get_attribute(
                        "src")
                except Exception as e:
                    img = ''

                # desc_html = soup.find(class_='product__price').find(class_='inner_props')
                try:
                    price = ''.join(
                        filter(str.isdigit, soup.find(class_='product__price').find(class_="font-bold").text))
                except Exception:
                    price = '0'

                try:
                    description = soup.find(id="product-desc-wrap").text
                except Exception:
                    description = ""

                try:
                    feature = soup.find(id="product-char-wrap")
                except Exception:
                    feature = ""

                try:
                    credit = soup.find(class_="product-installment-block")
                    has_credit = True
                    credit_monthly_amount = ''.join(filter(str.isdigit, credit.find(class_="installment__price").text))

                except Exception as e:
                    has_credit = False
                    credit_monthly_amount = ""

                try:
                    address = soup.find(class_="presence__address").text
                    delivery_info = soup.find(class_="type-info__text").find('span').text
                    phone_number = soup.find(class_="presence__phone").text
                except Exception:
                    address = ""
                    phone_number = ""
                    delivery_info = ""

                # id = browser.current_url.split('/')[-2]
                print(product_name)

                obj = {
                    'name': str(product_name),
                    'photo': str(img),
                    'price_amount': str(price),
                    'description': str(description),
                    'feature': str(feature),
                    'has_credit': has_credit,
                    'credit_monthly_amount': credit_monthly_amount,
                    'has_delivery': True,
                    'address': address,
                    'phone_number': phone_number,
                    'delivery_info': delivery_info,
                    'website': 'Texnomart',
                    'website_link': str(item_url)
                }
                requests.post('https://api.taqqoz.uz/v1/product/price/create/', data=obj)


def thr_prog(links, thr_ind=1):
    global main_result
    threads = []

    # Створюємо 5 потоків
    for i in range(thr_ind):
        thread = threading.Thread(target=prog, args=(links, i, thr_ind))
        threads.append(thread)
        thread.start()

    # Очікуємо завершення всіх потоків
    for thread in threads:
        thread.join()

