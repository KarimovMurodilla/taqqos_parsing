from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import json
import time
import requests

LINK = 'https://goodzone.uz'


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

    def ab(content):
        try:
            html = content.get_attribute('outerHTML')
            soup = BeautifulSoup(html, 'html.parser')
            items = soup.find('section', class_='catalog_catalogPageCard__D89oy').find(
                class_='mantine-Grid-root mantine-16fdnqw').find_all(class_='mantine-Grid-col mantine-b6e2c5')
        except Exception:
            items = []
        return items

    try:
        html = browser.page_source
        soup = BeautifulSoup(html, 'html.parser')
        page_count = int(soup.find(class_='catalog_productPagination__bpJ11 mantine-7o6j5m').find_all('button',
                                                                                                      'mantine-UnstyledButton-root')[
                             -2].text)
    except Exception as e:
        print(e)
        page_count = 1

    for ind in range(1, page_count + 1):
        button = browser.find_element(By.XPATH, f'//button[text()="{ind}"]')
        button.click()
        content = WebDriverWait(browser, 1).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'catalog_catalogPageCard__D89oy')))
        time.sleep(10)
        items = ab(content)

        print(f'page_count - {page_count}, page - {ind}')
        for item in items:
            try:
                item_title = item.find('a')
                item_url = LINK + item_title.get('href')
            except Exception as e:
                print(e)
                continue
            browser.get(item_url)

            time.sleep(10)

            html = browser.page_source
            soup = BeautifulSoup(html, 'html.parser')

            try:
                product_name = soup.find('p', class_='product-view_productViewsTitle__Nzlfn').text
            except Exception:
                continue

            try:
                img = soup.find(class_='product-view_productViewsImage__a7tEH mantine-1avyp1d').find_all('img')[-1][
                    'src']
            except Exception as e:
                print(e)
                img = ''

            try:
                price = ''.join(
                    filter(str.isdigit, soup.find('p', class_="product-view_productViewsPriceTitle__oPA8C").text))
            except Exception:
                price = '0'

            try:
                all_p = soup.find(class_="product-view_miniDescription__KCHUv").find_all('p')
                description = all_p[0].text
                for p in all_p:
                    text = p.text
                    if len(text) > 50:
                        description = text
                        break

            except Exception:
                description = ""

            try:
                features = soup.find(class_="table_characteristic").find('table').find('tbody').find_all('tr')
            except Exception as e:
                print(e)
                features = ""
            features_list = {}
            if features:
                for feature in features:
                    try:
                        features_list[feature.find_all('td')[0].text] = feature.find_all('td')[1].text
                    except Exception:
                        continue

            has_credit = False
            credit_monthly_amount = '0'
            address = "100011, Узбекистан, Адрес: г. Ташкент, массив Чиланзар-6, ТЦ Bunyodkor"
            phone_number = "+998 71 207 03 07"
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
                'website': 'Goodzone',
                'website_link': str(item_url)
            }
            print(product_name)
            requests.post('https://api.taqqoz.uz/v1/product/price/create/', data=obj)
