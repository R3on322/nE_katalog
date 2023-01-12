import requests
import json
from config import cookies_mvideo as cookies, headers_mvideo as headers
import os, math

class MvideoParser:

    def __init__(self, cat_id):
        self.cat_id = cat_id

    def get_data(self):

        if not os.path.exists('data/mvideo_pars'):
            os.mkdir('data/mvideo_pars')

        s = requests.Session()

        params = {
            'categoryId': self.cat_id,
            'offset': '0',
            'limit': '24',
            'filterParams': 'WyJ0b2xrby12LW5hbGljaGlpIiwiLTEyIiwiZGEiXQ==',
            'doTranslit': 'true',
        }

        response = s.get('https://www.mvideo.ru/bff/products/listing', params=params, cookies=cookies,
                                headers=headers).json()

        total_items = response.get('body').get('total')

        if total_items is None:
            return 'No items there :('

        pages_count = math.ceil(total_items / 24)

        products_description = {}
        products_prices = {}

        for i in range(pages_count):
            offset = f'{i * 24}'
            params = {
                'categoryId': self.cat_id,
                'offset': offset,
                'limit': '24',
                'filterParams': 'WyJ0b2xrby12LW5hbGljaGlpIiwiLTEyIiwiZGEiXQ==',
                'doTranslit': 'true',
            }

            response = requests.get('https://www.mvideo.ru/bff/products/listing', params=params, cookies=cookies,
                                    headers=headers).json()

            products_ids_list = response.get('body').get('products')

            json_data = {
                'productIds': products_ids_list,
                'mediaTypes': [
                    'images',
                ],
                'category': True,
                'status': True,
                'brand': True,
                'propertyTypes': [
                    'KEY',
                ],
                'propertiesConfig': {
                    'propertiesPortionSize': 5,
                },
                'multioffer': False,
            }

            response = s.post('https://www.mvideo.ru/bff/product-details/list', cookies=cookies, headers=headers,
                                     json=json_data, params=params).json()

            products_description[f'Page: {i + 1}'] = response.get('body').get('products')

            products_ids_str = ','.join(products_ids_list)

            params = {
                'productIds': products_ids_str,
                'addBonusRubles': 'true',
                'isPromoApplied': 'true',
            }

            response = s.get('https://www.mvideo.ru/bff/products/prices', params=params, cookies=cookies,
                                    headers=headers).json()

            products_prices_get = response.get('body').get("materialPrices")

            for card in products_prices_get:
                products_id = card.get('price').get('productId')
                products_sale_price = card.get('price').get('salePrice')

                products_prices[products_id] = {
                    'sale_price' : products_sale_price,
                }

            print(f'[+] Finished {i + 1} of {pages_count} pages')

        with open(f'data/mvideo_pars/{self.cat_id}_products_description.json', 'w' , encoding='UTF-8') as file:
            json.dump(products_description, file, indent=4, ensure_ascii=False)
        with open(f'data/mvideo_pars/{self.cat_id}_products_prices.json', 'w', encoding='UTF-8') as file:
            json.dump(products_prices, file, indent=4, ensure_ascii=False)


    def merge_data(self):
        with open(f'data/mvideo_pars/{self.cat_id}_products_description.json', encoding='UTF-8') as file:
            products_data = json.load(file)

        with open(f'data/mvideo_pars/{self.cat_id}_products_prices.json', encoding='UTF-8') as file:
            products_prices = json.load(file)

        sorted_list_products = []

        for page in products_data.values():
            for product in page:
                product_dict = {}
                product_id = product['productId']
                if product_id in products_prices:
                    product_sale_price = products_prices[product_id]['sale_price']
                product_dict['ID'] = int(product_id)
                product_dict['NAME'] = product['name']
                product_dict['MODEL'] = product['modelName']
                product_dict['PRICE'] = product_sale_price
                product_dict['URL'] = f'https://www.mvideo.ru/products/{product["nameTranslit"]}-{product_id}'
                sorted_list_products.append(product_dict)

        with open(f'data/mvideo_pars/{categories_dict[self.cat_id]}.json', 'w', encoding='UTF-8') as file:
            json.dump(sorted_list_products, file, indent=4, ensure_ascii=False)
            os.remove(f'data/mvideo_pars/{self.cat_id}_products_description.json')
            os.remove(f'data/mvideo_pars/{self.cat_id}_products_prices.json')

categories_dict = {
    '5429' : 'Видеокарты',
    '5431' : 'Процессоры',
    '5432' :'Материнские платы',
    '5433' : 'Оперативная память',
    '5436' : 'Жёсткие диски HDD SSD',
    '5435' : 'Блоки питания'
}


def main(category):
    new_cat_dict = {v:k for k,v in categories_dict.items()}
    try:
        cat_id = new_cat_dict[category]
        M = MvideoParser(str(cat_id))
        M.get_data()
        M.merge_data()
    except Exception:
        print('Такой категории не существует')
        return 'Такой категории не существует'


if __name__ == '__main__':
    main('Видеокарты')