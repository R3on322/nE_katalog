import requests
from config import cookies_regard as cookies, headers_regard as headers


r = requests.Session()
json_data = {
            'start': 0,
            'length': 24,
            'scope': {
                'byCategory': '1013', #видеокарты
                'orderByName': 'asc'
            },
        }

response = r.get('https://www.regard.ru/api/site/goods/list',
                 cookies=cookies,
                 headers=headers,
                 json=json_data).json()

def list_of_memory():
    a = response.get('new_filters')[3].get('values')[2].get('values')
    memory_dict = {}
    for i in a:
        size = int(i['title'].split()[0])
        if 1 <= size <= 48:
            memory_dict[size] = i['value']
    return memory_dict

def main():
    list_of_memory()


if __name__ == '__main__':
    main()