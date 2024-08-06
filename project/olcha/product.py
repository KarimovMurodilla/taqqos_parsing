import requests


def prog(links):
    for link in links:
        response = requests.get(link)
        response_json = response.json()

        for product in response_json['data']['products']:
            product_name = product['name_ru']
            img = product['main_image']
            price = product['discount_price']
            description = product['short_description_ru']
            phone_number = "+998 (71) 202-20-21"
            address = "Козитарнов, Ташкент"
            item_url = f"https://olcha.uz/ru/product/view/{product['alias']}"
            has_credit = False
            has_delivery = True
            features_list = None
            credit_monthly_amount = 0
            delivery_info = None

            obj = {
                'name': str(product_name),
                'photo': str(img),
                'price_amount': str(price),
                'description': str(description),
                'features': features_list,
                'has_credit': has_credit,
                'credit_monthly_amount': credit_monthly_amount,
                'has_delivery': has_delivery,
                'address': address,
                'phone_number': phone_number,
                'delivery_info': delivery_info,
                'website': 'Olcha',
                'website_link': str(item_url)
            }
            print(product_name, img)
            # requests.post('https://api.taqqoz.uz/v1/product/price/create/', data=obj)
            requests.post('http://localhost:8000/v1/product/price/create/', data=obj)
