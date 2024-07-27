import time
import requests
from bs4 import BeautifulSoup

from schemas import CategorySchema
from services import create_category

LINK = 'https://mobile.olcha.uz/api/v2/categories'


def prog():
    response = requests.get(LINK)
    response_json = response.json()
    
    categories = response_json['data']['categories']

    for category in categories:
        category_url = f"https://mobile.olcha.uz/api/v2/products?category={category['alias']}&per_page=24"
        data = {
            "name": category['name_ru'],
            "url": category_url,
            "website": "olcha"
        }
        data = CategorySchema(**data)
        create_category(data=data)

        if category['children']:
            for child in category['children']:
                category_url = f"https://mobile.olcha.uz/api/v2/products?category={child['alias']}&per_page=24"
                data = {
                    "name": child['name_ru'],
                    "url": category_url,
                    "website": "olcha"
                }
                data = CategorySchema(**data)
                create_category(data=data)
