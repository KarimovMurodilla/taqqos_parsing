from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import json
import time
import requests
import traceback

LINK = 'https://mediapark.uz'


def browser_init():
    chrome_options = Options()
    chrome_options.set_capability("pageLoadStrategy", "normal")  # Try 'normal' or 'eager' instead of 'none'
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--window-size=1920,1080')
    chrome_options.add_argument('--remote-debugging-port=9222')  # Useful for debugging
    chrome_options.add_argument('--enable-logging')
    chrome_options.add_argument('--v=1')
    
    browser = webdriver.Chrome(options=chrome_options)
    return browser


def prog(links):
    for link in links:
        browser = browser_init()
        browser.get(link)
        print("Link is:", link)
        time.sleep(5)

        def ab():

            is_page_loading = True

            while is_page_loading:
                html = browser.page_source
                soup = BeautifulSoup(html, 'html.parser')
                try:
                    items = soup.find_all('a', class_='product-cart')
                    is_page_loading = False
                    break
                except Exception as e:
                    print(e)
                    time.sleep(1)
            return items
        
        try:
            page_count = int(
                browser.find_element(By.CLASS_NAME, 'pagination').find_elements(By.TAG_NAME, 'li')[-2].text)
        except Exception as e:
            traceback.print_exc()
            page_count = 1


        for ind in range(1, page_count + 1):
            tot_url = link + f'?page={ind}'
            browser.get(tot_url)
            # time.sleep(20)
            items = ab()

            print(f'page_count - {page_count}, page - {ind}')
            for item in items:
                item_url_half = item.get('href')
                item_url = LINK + item_url_half
                browser.get(item_url)

                time.sleep(500)

                html = browser.page_source
                soup = BeautifulSoup(html, 'html.parser')

                try:
                    product_name = soup.find('div', class_='flex items-center justify-between').find('h1').get_text(strip=True)
                except Exception:
                    traceback.print_exc()
                    continue

                try:
                    lazy_load = soup.find('div', class_='LazyLoad is-visible', attrs={'style': "height: 490px;"})
                    img = lazy_load.find('img')['src']
                except Exception as e:
                    traceback.print_exc()
                    img = ''

                try:
                    price = ''.join(
                        filter(str.isdigit, soup.find('h3', class_='text-[22px] font-[700] text-dark').text))
                except Exception as e:
                    traceback.print_exc()
                    price = '0'

                try:
                    description = soup.find(class_="rich ql-editor").text
                except Exception as e:
                    traceback.print_exc()
                    description = ""

                try:
                    features = soup.find(class_="mt-[12px] flex flex-col laptop:gap-[12px]").find_all(
                        class_='grid grid-cols-2 items-center gap-[10px]')
                except Exception as e:
                    traceback.print_exc()
                    features = ""
                features_list = {}
                if features:
                    for feature in features:
                        try:
                            features_list[
                                feature.find(
                                    'span',
                                    class_='tablet:text-[14px] text-gray font-[400] mobileS:text-[12px] flex gap-[8px]'
                                ).text
                            ] = feature.find(
                                class_='tablet:text-[14px] text-dark font-[400] mobileS:text-[12px] truncate').text
                        except Exception:
                            continue

                try:
                    has_credit = True
                    credit_monthly_amount = ''.join(
                        filter(str.isdigit, soup.find_all('span', class_="mr-[4px]")[-1].text))

                except Exception as e:
                    traceback.print_exc()
                    has_credit = False
                    credit_monthly_amount = ""

                try:
                    address = ', '.join(
                        [e.text for e in soup.find_all('p', class_="text-gray text-[14px] font-[400] leading-[150%]")])
                    delivery_info = "Бесплатнo"
                    phone_number = ""
                except Exception as e:
                    traceback.print_exc()
                    address = "Ташкент, Шайхонтохурский район, ул. Караташ, 11А, Ташкент, Юнусабадский район, ул.Ш.Рашидова 16A, Ташкент, Мирзо-Улугбекский район, проспект Мирзо-Улугбек, ул. Т.Малик, дом 3A, Ташкент, Учтепинский район, улица Фархадская, дом 31А ,  Ташкент, Юнусабадский район, массив Юнусабад, 19-й квартал, 119"
                    phone_number = "+998 71 203 33 33"
                    delivery_info = ""

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
                    'website': 'Mediapark',
                    'website_link': str(item_url)
                }
                print("Mediapark,", product_name)

                r = requests.post('https://api.taqqoz.uz/v1/product/price/create/', data=obj)
                print("Response status:", r.status_code)
