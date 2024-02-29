from celery_config import app as celery_app
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import json
import time
import requests

LINK = 'https://maxcom.uz'


def browser_init():
    chrome_options = Options()
    chrome_options.set_capability("pageLoadStrategy", "none")
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--window-size=1920,1080')  
    browser = webdriver.Chrome(options=chrome_options)
    return browser


def parser(link):
    browser = browser_init()
    browser.get(link)
    time.sleep(15)
    html = browser.page_source
    soup = BeautifulSoup(html, 'html.parser')

    def ab(browser):
        i = 0
        items = []
        while i < 3:
            html = browser.page_source
            soup = BeautifulSoup(html, 'html.parser')
            try:
                items = soup.find(class_='ps-shopping-product').find_all(class_='ps-product')
                break
            except Exception as e:
                print(e)
                i += 1
                time.sleep(1)
        return items
    
    try:
        page_count = int(soup.find(class_='ps-pagination').find('ul', class_='pagination').find_all('li')[-2].text)
    except Exception as e:
        print(e)
        page_count = 1
    
    for ind in range(1, page_count+1):
        tot_url = link+f'?page={ind}'
        browser.get(tot_url)
        time.sleep(10)

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
                product_name = soup.find(class_='ps-product__info').find('h1').text
            except Exception:
                continue

            try:
                img = soup.find(class_='ps-product__gallery').find('img')['src']
            except Exception as e:
                print(e)
                img = ''
            
            try:
                price =''.join(filter(str.isdigit, soup.find(class_='ps-product__info').find('h4', class_='ps-product__price').text)) 
            except Exception:
                price = '0'
            
            has_credit = False
            credit_monthly_amount = '0'

            try:
                features = soup.find(class_="ps-tabs").find(id="tab-2").find('table').find('tbody').find_all('tr')
            except Exception as e:
                print(e)
                features = ""
            features_list = {}
            if features:
                for feature in features:
                    try:
                        features_list[feature.find_all('td')[0].text] = feature.find_all('td')[1].text
                    except Exception as e:
                        print(e)
                        continue
            
            try:
                description = str(soup.find(id="tab-1").find(class_="ps-document").text)
                if len(description) < 10:
                    description = None
            except Exception as e:
                print(e)
                description = None     

            address = 'г.Ташкент,Шайхантохурский район,ул.Бунёдкор, 8A '
            phone_number = "+998 (71) 200 27 07"
            delivery_info = "Доставка по Узбекистану"
            has_delivery = True

            obj = {
                'name' : str(product_name),
                'photo' : str(img),
                'price_amount': str(price),
                'description' : description,
                'features' : json.dumps(features_list),
                'has_credit' : has_credit, 
                'credit_monthly_amount' : credit_monthly_amount,
                'has_delivery': has_delivery,
                'address': address,
                'phone_number': phone_number,
                'delivery_info': delivery_info,
                'website': 'Maxcom',
                'website_link': str(item_url)
            }
            print(f"Maxcom, {product_name}")
            try:
                r = requests.post('https://api.taqqoz.uz/v1/product/price/create/', data=obj, timeout=120)
                print(r.status_code)
            except Exception as e:
                print(e)


@celery_app.task
def category_parse():
    data = [{"name": "Ноутбуки", "url": "https://maxcom.uz/catalog/laptop", "website": "maxcom"}, {"name": "Сумки для ноутбуков", "url": "https://maxcom.uz/catalog/laptop%20bag", "website": "maxcom"}, {"name": "Дорожные сумки", "url": "https://maxcom.uz/catalog/travel%20bag", "website": "maxcom"}, {"name": "Аккумуляторы для ноутбука", "url": "https://maxcom.uz/catalog/akkumulatorydlyanoutbukov", "website": "maxcom"}, {"name": "Телевизоры", "url": "https://maxcom.uz/catalog/tv", "website": "maxcom"}, {"name": "Стереосистема", "url": "https://maxcom.uz/catalog/speakers", "website": "maxcom"}, {"name": "ТВ-приставки", "url": "https://maxcom.uz/catalog/TVset-top", "website": "maxcom"}, {"name": "Портативная акустика", "url": "https://maxcom.uz/catalog/portableSpeakerSystems", "website": "maxcom"}, {"name": "TV комплектующие и аксессуары", "url": "https://maxcom.uz/catalog/tv-acessories", "website": "maxcom"}, {"name": "Радиотелефоны", "url": "https://maxcom.uz/catalog/radiotelephone", "website": "maxcom"}, {"name": "Факсы", "url": "https://maxcom.uz/catalog/fax", "website": "maxcom"}, {"name": "IP телефон", "url": "https://maxcom.uz/catalog/networkphone", "website": "maxcom"}, {"name": "Конференц устройства", "url": "https://maxcom.uz/catalog/ConferencingHardware", "website": "maxcom"}, {"name": "Модули резервирования", "url": "https://maxcom.uz/catalog/UCMSeries", "website": "maxcom"}, {"name": "Ретрансляторы", "url": "https://maxcom.uz/catalog/dectcordless", "website": "maxcom"}, {"name": "Шлюзы", "url": "https://maxcom.uz/catalog/AnalogVoIP", "website": "maxcom"}, {"name": "Проводные телефоны", "url": "https://maxcom.uz/catalog/wirephone", "website": "maxcom"}, {"name": "Домофоны", "url": "https://maxcom.uz/catalog/domofony", "website": "maxcom"}, {"name": "Комплект клавиатура и мышка", "url": "https://maxcom.uz/catalog/gamingkit", "website": "maxcom"}, {"name": "Принтеры и МФУ", "url": "https://maxcom.uz/catalog/printers", "website": "maxcom"}, {"name": "Чернила", "url": "https://maxcom.uz/catalog/ink", "website": "maxcom"}, {"name": "Сканеры", "url": "https://maxcom.uz/catalog/scanner", "website": "maxcom"}, {"name": "Комплектующие для принтеров и МФУ", "url": "https://maxcom.uz/catalog/accessoriesforprinters", "website": "maxcom"}, {"name": "Картриджи", "url": "https://maxcom.uz/catalog/cartridge", "website": "maxcom"}, {"name": "Планшеты", "url": "https://maxcom.uz/catalog/cell%20%20tablet", "website": "maxcom"}, {"name": "Кнопочные телефоны", "url": "https://maxcom.uz/catalog/button%20phones", "website": "maxcom"}, {"name": "Фен", "url": "https://maxcom.uz/catalog/fan", "website": "maxcom"}, {"name": "Машинки для стрижки", "url": "https://maxcom.uz/catalog/clipper", "website": "maxcom"}, {"name": "Электрические зубные щетки", "url": "https://maxcom.uz/catalog/an-electric-toothbrush", "website": "maxcom"}, {"name": "Электробритвы", "url": "https://maxcom.uz/catalog/fa-electric-shaver", "website": "maxcom"}, {"name": "Соковыжималки", "url": "https://maxcom.uz/catalog/juicer", "website": "maxcom"}, {"name": "Мясорубки", "url": "https://maxcom.uz/catalog/meat%20grinder", "website": "maxcom"}, {"name": "Блендеры", "url": "https://maxcom.uz/catalog/blender", "website": "maxcom"}, {"name": "Миксеры", "url": "https://maxcom.uz/catalog/mixer", "website": "maxcom"}, {"name": "Утюги", "url": "https://maxcom.uz/catalog/iron", "website": "maxcom"}, {"name": "Чайники и термоподы", "url": "https://maxcom.uz/catalog/teapot", "website": "maxcom"}, {"name": "Хлебопечь", "url": "https://maxcom.uz/catalog/breadmachine", "website": "maxcom"}, {"name": "Эпиляторы", "url": "https://maxcom.uz/catalog/epilator", "website": "maxcom"}, {"name": "Мультистайлеры", "url": "https://maxcom.uz/catalog/multistyler", "website": "maxcom"}, {"name": "Электропечь", "url": "https://maxcom.uz/catalog/electric%20furnace", "website": "maxcom"}, {"name": "Увлажнители, очистители воздуха", "url": "https://maxcom.uz/catalog/airpurifier", "website": "maxcom"}, {"name": "Кофемашины", "url": "https://maxcom.uz/catalog/coffee%20machine", "website": "maxcom"}, {"name": "Весы", "url": "https://maxcom.uz/catalog/scales", "website": "maxcom"}, {"name": "Машинки для удаления катышков", "url": "https://maxcom.uz/catalog/machine%20to%20remove%20the%20pellets", "website": "maxcom"}, {"name": "Массажёры", "url": "https://maxcom.uz/catalog/Masseur", "website": "maxcom"}, {"name": "Обогреватели воздуха", "url": "https://maxcom.uz/catalog/air%20heater", "website": "maxcom"}, {"name": "Вентиляторы", "url": "https://maxcom.uz/catalog/air%20fan", "website": "maxcom"}, {"name": "Термосы", "url": "https://maxcom.uz/catalog/thermos", "website": "maxcom"}, {"name": "Измерительные приборы", "url": "https://maxcom.uz/catalog/measurement%20instrumentation", "website": "maxcom"}, {"name": "Рисоварки", "url": "https://maxcom.uz/catalog/risovarka", "website": "maxcom"}, {"name": "Другие бытовые товары", "url": "https://maxcom.uz/catalog/other%20household%20goods", "website": "maxcom"}, {"name": "Плиты", "url": "https://maxcom.uz/catalog/slabs", "website": "maxcom"}, {"name": "Комплектующие на UPS", "url": "https://maxcom.uz/catalog/battery-full", "website": "maxcom"}, {"name": "Источники бесперебойного питания (ИБП)", "url": "https://maxcom.uz/catalog/ibp", "website": "maxcom"}, {"name": "Батарейные шкафы", "url": "https://maxcom.uz/catalog/batterycabinet", "website": "maxcom"}, {"name": "Зарядные устройства", "url": "https://maxcom.uz/catalog/batterycharger", "website": "maxcom"}, {"name": "Батарейки", "url": "https://maxcom.uz/catalog/small%20battery", "website": "maxcom"}, {"name": "Внешние аккумуляторы", "url": "https://maxcom.uz/catalog/external%20battery", "website": "maxcom"}, {"name": "Настенные кондиционеры", "url": "https://maxcom.uz/catalog/nastennye-konditsionery", "website": "maxcom"}, {"name": "Напольные кондиционеры", "url": "https://maxcom.uz/catalog/floorconditioning", "website": "maxcom"}, {"name": "Микроволновая печь", "url": "https://maxcom.uz/catalog/microwave", "website": "maxcom"}, {"name": "Стиральные машины", "url": "https://maxcom.uz/catalog/stiralniyemashiny", "website": "maxcom"}, {"name": "Пылесосы", "url": "https://maxcom.uz/catalog/vacuum%20cleaner", "website": "maxcom"}, {"name": "Вытяжки", "url": "https://maxcom.uz/catalog/hoods", "website": "maxcom"}, {"name": "Духовки", "url": "https://maxcom.uz/catalog/duxovers", "website": "maxcom"}, {"name": "Посудамоечные машины", "url": "https://maxcom.uz/catalog/washingmachines", "website": "maxcom"}, {"name": "Холодильники", "url": "https://maxcom.uz/catalog/Fridges", "website": "maxcom"}, {"name": "Морозильники", "url": "https://maxcom.uz/catalog/freezers", "website": "maxcom"}, {"name": "Фотоаппарапы", "url": "https://maxcom.uz/catalog/photocamera", "website": "maxcom"}, {"name": "Диктофоны", "url": "https://maxcom.uz/catalog/dictaphone", "website": "maxcom"}, {"name": "Видеокамеры", "url": "https://maxcom.uz/catalog/camera-recorder1", "website": "maxcom"}, {"name": "Экшн-камеры", "url": "https://maxcom.uz/catalog/actioncamera", "website": "maxcom"}, {"name": "Аксессуары для фото-видео техники", "url": "https://maxcom.uz/catalog/accessoriesforphotoequipment", "website": "maxcom"}, {"name": "Канцелярия", "url": "https://maxcom.uz/catalog/office%20supplies", "website": "maxcom"}, {"name": "Офисные кресла", "url": "https://maxcom.uz/catalog/ofisnye-kresla", "website": "maxcom"}, {"name": "Видеорегистраторы", "url": "https://maxcom.uz/catalog/car%20dashboard%20camera", "website": "maxcom"}, {"name": "Другие автотовары", "url": "https://maxcom.uz/catalog/other%20automotive%20products", "website": "maxcom"}, {"name": "Портативная автотехника", "url": "https://maxcom.uz/catalog/portable%20automotive%20equipment", "website": "maxcom"}, {"name": "Проекторы и экраны", "url": "https://maxcom.uz/catalog/projectors", "website": "maxcom"}, {"name": "Инфокиоски", "url": "https://maxcom.uz/catalog/infokiosk", "website": "maxcom"}, {"name": "Аксессуары для телефонов", "url": "https://maxcom.uz/catalog/cell%20phones%20accessories", "website": "maxcom"}, {"name": "Аксессуары для планшетов", "url": "https://maxcom.uz/catalog/accessories%20for%20tablets", "website": "maxcom"}, {"name": "IP / PTZ видеокамеры", "url": "https://maxcom.uz/catalog/ipcam", "website": "maxcom"}, {"name": "NVR видеорегистраторы", "url": "https://maxcom.uz/catalog/NvrDvr", "website": "maxcom"}, {"name": "Комплект", "url": "https://maxcom.uz/catalog/webcamdvr", "website": "maxcom"}, {"name": "Комплектующие", "url": "https://maxcom.uz/catalog/componentparts", "website": "maxcom"}, {"name": "Наручные часы", "url": "https://maxcom.uz/catalog/naruchnye-chasy", "website": "maxcom"}, {"name": "Сантехника", "url": "https://maxcom.uz/catalog/santekhnika", "website": "maxcom"}, {"name": "Швейные машины", "url": "https://maxcom.uz/catalog/shveynye-mashiny", "website": "maxcom"}, {"name": "Интерактивные доски", "url": "https://maxcom.uz/catalog/interaktivnye-doski", "website": "maxcom"}, {"name": "Портативная техника", "url": "https://maxcom.uz/catalog/car%20portable%20equipment", "website": "maxcom"}, {"name": "Спортивные тренажёры", "url": "https://maxcom.uz/catalog/sport%20trainer", "website": "maxcom"}, {"name": "Настольные игры, головоломки", "url": "https://maxcom.uz/catalog/nastolnye-igry-golovolomki", "website": "maxcom"}, {"name": "Фонарики", "url": "https://maxcom.uz/catalog/Lantern", "website": "maxcom"}, {"name": "Роботы", "url": "https://maxcom.uz/catalog/roboty", "website": "maxcom"}, {"name": "Смарт-часы", "url": "https://maxcom.uz/catalog/smart%20watch", "website": "maxcom"}, {"name": "Фитнес-браслеты", "url": "https://maxcom.uz/catalog/fitness%20bracelet", "website": "maxcom"}, {"name": "Аксессуары для часов", "url": "https://maxcom.uz/catalog/accessories%20for%20hours", "website": "maxcom"}, {"name": "Антибликовые очки", "url": "https://maxcom.uz/catalog/anti%20glare%20glasses", "website": "maxcom"}, {"name": "Солнцезащитные очки", "url": "https://maxcom.uz/catalog/sunglasses", "website": "maxcom"}, {"name": "Настольные лампы", "url": "https://maxcom.uz/catalog/table%20lamp", "website": "maxcom"}, {"name": "Ночник", "url": "https://maxcom.uz/catalog/nightlight", "website": "maxcom"}, {"name": "Светодиодные лампы", "url": "https://maxcom.uz/catalog/led%20lamp", "website": "maxcom"}, {"name": "Подушки", "url": "https://maxcom.uz/catalog/home%20pillow", "website": "maxcom"}, {"name": "Полотенца", "url": "https://maxcom.uz/catalog/home%20towels", "website": "maxcom"}, {"name": "Кошельки и бумажники", "url": "https://maxcom.uz/catalog/Wallet", "website": "maxcom"}, {"name": "Головные уборы", "url": "https://maxcom.uz/catalog/headdress%20hat", "website": "maxcom"}, {"name": "Обувь", "url": "https://maxcom.uz/catalog/shoes", "website": "maxcom"}, {"name": "Аккумуляторы и батарейки", "url": "https://maxcom.uz/catalog/akkumulyatory-i-batareyki", "website": "maxcom"}, {"name": "Очки", "url": "https://maxcom.uz/catalog/ochki", "website": "maxcom"}, {"name": "Освещение", "url": "https://maxcom.uz/catalog/osveshchenie", "website": "maxcom"}, {"name": "Сейфы", "url": "https://maxcom.uz/catalog/seyfy", "website": "maxcom"}, {"name": "Техника для кухни", "url": "https://maxcom.uz/catalog/tekhnika-dlya-kukhni", "website": "maxcom"}, {"name": "Техника для красоты и здоровья", "url": "https://maxcom.uz/catalog/tekhnika-dlya-krasoty-i-zdorovya", "website": "maxcom"}, {"name": "Домашний текстиль", "url": "https://maxcom.uz/catalog/domashniy-tekstil", "website": "maxcom"}, {"name": "Сумки и чехлы", "url": "https://maxcom.uz/catalog/sumki-i-chekhly", "website": "maxcom"}, {"name": "Одежда", "url": "https://maxcom.uz/catalog/odezhda", "website": "maxcom"}, {"name": "Компьютерные аксессуары", "url": "https://maxcom.uz/catalog/kompyuternye-aksessuary", "website": "maxcom"}, {"name": "Всё для оптики", "url": "https://maxcom.uz/catalog/vse-dlya-optiki", "website": "maxcom"}, {"name": "Все для меди", "url": "https://maxcom.uz/catalog/vse-dlya-medi", "website": "maxcom"}, {"name": "Коробы пластмассовые", "url": "https://maxcom.uz/catalog/koroby-plastmassovye", "website": "maxcom"}, {"name": "Кондиционеры", "url": "https://maxcom.uz/catalog/konditsionery", "website": "maxcom"}, {"name": "Cтационарные телефоны", "url": "https://maxcom.uz/catalog/ctatsionarnye-telefony", "website": "maxcom"}, {"name": "Программное обеспечение", "url": "https://maxcom.uz/catalog/programmnoe-obespechenie", "website": "maxcom"}, {"name": "Мониторы", "url": "https://maxcom.uz/catalog/monitory", "website": "maxcom"}]
    for link in data:
        parser(link['url'])
