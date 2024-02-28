from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import json
import time
import requests

LINK = 'https://elmakon.uz'


def browser_init():
    chrome_options = Options()
    chrome_options.set_capability("pageLoadStrategy", "none")
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--window-size=1920,1080')
    browser = webdriver.Chrome(options=chrome_options)

    return browser


def prog(link):
    browser = browser_init()
    browser.get(link)
    time.sleep(10)
    html = browser.page_source
    soup = BeautifulSoup(html, 'html.parser')

    def ab():

        is_page_loading = True

        while is_page_loading:
            html = browser.page_source
            soup = BeautifulSoup(html, 'html.parser')
            try:
                items = soup.find(id='categories_view_pagination_contents').find_all(class_='ty-column4')
                is_page_loading = False
                break
            except Exception:
                time.sleep(1)
        return items

    try:
        page_count = int(soup.find(
            id='ut2_pagination_block_bottom'
        ).find(class_='ty-pagination__items').find_all(
            class_='ty-pagination__item')[-1].text)
    except Exception as e:
        print(e)
        page_count = 1

    for ind in range(1, page_count + 1):
        tot_url = link + f'page-{ind}/'
        browser.get(tot_url)
        time.sleep(10)

        items = ab()

        print(f'page_count - {page_count}, page - {ind}')
        for item in items:
            item_title = item.find(class_='ut2-gl__body').find(class_='ut2-gl__content').find(class_='ut2-gl__name')
            item_url = item_title.find('a').get('href')
            browser.get(item_url)

            time.sleep(5)

            html = browser.page_source
            soup = BeautifulSoup(html, 'html.parser')

            try:
                product_name = soup.find('h1', class_='ut2-pb__title').find('bdi').text
            except Exception:
                continue

            try:
                img = browser.find_element(By.CLASS_NAME, 'ty-product-img').find_element(By.TAG_NAME,
                                                                                         'img').get_attribute("src")
            except Exception:
                img = ''

            try:
                price = ''.join(filter(str.isdigit, soup.find(class_='ty-price').find(class_="ty-price-num").text))
            except Exception:
                price = '0'

            try:
                description = soup.find(id="content_description").text
            except Exception:
                description = ""

            try:
                features = soup.find(class_="ty-features-list").find_all(class_='ty-control-group')
            except Exception:
                features = ""
            features_list = {}
            if features:
                for feature in features:
                    try:
                        features_list[
                            feature.find(
                                'span', class_='ty-product-feature__label'
                            ).text
                        ] = feature.find_all('span')[-1].text
                    except Exception:
                        continue

            try:
                address = ', '.join(
                    [e.text.rstrip().lstrip() for e in soup.find_all(class_="ty-warehouses-store__address")])
                delivery_info = ''
                phone_number = soup.find(class_="ut2-vendor-block__phone").text
            except Exception:
                address = ""
                phone_number = ""
                delivery_info = ""

            try:
                button = browser.find_element(By.ID, 'opener_fast_installment')
                button.click()
                time.sleep(10)
                credit = WebDriverWait(browser, 1).until(
                    EC.presence_of_element_located((By.ID, "content_fast_installment"))
                )
                has_credit = True
                credit_monthly_amount = ''.join(filter(str.isdigit, credit.find_element(By.CLASS_NAME,
                                                                                        "fast-installment-options-item-head-payment").find_element(
                    By.TAG_NAME, "span").text))

            except Exception:
                has_credit = False
                credit_monthly_amount = ""

            obj = {
                'name': str(product_name),
                'photo': str(img),
                'price_amount': str(price),
                'description': str(description),
                'features': json.dumps(features_list),
                'has_credit': has_credit,
                'credit_monthly_amount': credit_monthly_amount,
                'has_delivery': True,
                'address': address,
                'phone_number': phone_number,
                'delivery_info': delivery_info,
                'website': 'Elmakon',
                'website_link': str(item_url)
            }
            print(product_name)
            requests.post('https://api.taqqoz.uz/v1/product/price/create/', data=obj)
