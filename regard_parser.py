import math
from config import cookies_regard as cookies, headers_regard as headers
import requests
import json
import os
from datetime import date
from get_list_of_prod import list_of_memory

class RegardParser:

    def __init__(self, cat_id: str, list_manufacture: list, list_price: list, list_memory: list):
        self.cat_id = cat_id
        self.list_manufacture = list_manufacture
        self.list_price = list_price
        self.list_memory = list_memory

    def get_data(self):
        if not os.path.exists('data/regard_pars'):
            os.mkdir('data/regard_pars')
        s = requests.Session()
        json_data = {
            'start': 0,
            'length': 24,
            'scope': {
                'byCategory': self.cat_id,
                'orderByName': 'asc'
            },
        }
        self.filter_data(json_data)
        response = s.post('https://www.regard.ru/api/site/goods/list',
                          cookies=cookies,
                          headers=headers,
                          json=json_data).json()
        total_pages = response.get('recordsFiltered')
        if total_pages is None:
            return 'No items there :('
        pages_count = math.ceil(total_pages / 24)
        # print(json_data)
        products_ids = {}
        for i in range(pages_count):
            start = f'{i * 24}'
            json_data['start'] = start
            response = s.post('https://www.regard.ru/api/site/goods/list',
                              cookies=cookies,
                              headers=headers,
                              json=json_data).json()
            product_ids_list = response.get('data')
            products_ids[f'Page: {i + 1}'] = product_ids_list
            print(f'[+] Finished {i + 1} of {pages_count} pages')
        self.save_data(products_ids)

    def filter_data(self, json_data : dict):
        if len(self.list_memory) >= 1:
            json_data['scope'].update({'byChar': {'69': {'values': [list_of_memory()[i] for i in self.list_memory]}}})
        if self.list_manufacture:
            json_data['scope'].update({'byVendor': {'values': self.list_manufacture, 'except': False}})
        if len(self.list_price) == 2 :
            if self.list_price[0] > self.list_price[1]:
                json_data['scope'].update({'byPrice': {'min': self.list_price[1], 'max': self.list_price[0]}})
            else:
                json_data['scope'].update({'byPrice': {'min': self.list_price[0], 'max': self.list_price[1]}})

        return json_data

    def save_data(self, product_data : dict):
        sorted_list_products = []
        for i in product_data.values():
            for product in i:
                product_dict = {}
                product_dict['ID'] = product['id']
                product_dict['NAME'] = product['full_title']
                product_dict['MODEL'] = product['title']
                product_dict['PRICE'] = product['price']
                product_dict['URL'] = f'https://www.regard.ru/product/{product["id"]}/{product["seo_url"]}'
                sorted_list_products.append(product_dict)

        with open(f'data/regard_pars/{categories_dict[self.cat_id]}.json', 'w', encoding='UTF-8') as file:
            json.dump(sorted_list_products, file, indent=4, ensure_ascii=False)

categories_dict = {
    '1013': 'Видеокарты',
    # '1001': 'Процессоры',
    # '1000': 'Материнские платы',
    # '1010': 'Оперативная память',
    # '1014': 'Жёсткие диски',
    # '1225': 'Блоки питания',
    # '1015': 'SSD'
}
def main(category, list_manufacture=[], list_price=[], list_memory=[]):
    new_cat_dict = {v: k for k, v in categories_dict.items()}
    try:
        cat_id = new_cat_dict[category]
        p = RegardParser(str(cat_id), list_manufacture, list_price, list_memory)
        p.get_data()
    except Exception:
        print('Такой категории не существует')
        return 'Такой категории не существует'

if __name__ == '__main__':
    main('Видеокарты',list_manufacture=[],list_price=[500000, 100000], list_memory=[])