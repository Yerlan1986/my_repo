import requests
import json
import urllib.parse
import os
import pandas as pd

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                  'AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/128.0.0.0 Safari/537.36 OPR/114.0.0.0',
    'accept': '*/*'
}

search_data = input('Введите текст для поиска товаров на WB: ') # запрашиваем у пользователя параментры для поиска товаров
encode_search_data = urllib.parse.quote(search_data) # преобразуем текст в формат URL для ссылки
filename = f'Results ({search_data})' # создает файл с результатами


def parser (encode_search_data):

    for page in range(1, 51): # 50 страниц, т.к. WB отдает только 50 страниц результатов поиска
        search_url = ('https://search.wb.ru/exactmatch/sng/common/v7/' # API запрос на получение ответа сервера в виде json файла
                       'search?ab_testing=false'
                       '&appType=1'
                       '&curr=rub'
                       '&dest=123589446'
                       f'&page={page}' # параметры для пагинации
                       f'&query={encode_search_data}' # передаем параметры для поиска
                       '&resultset=catalog'
                       '&sort=rate'
                       '&spp=30'
                       '&suppressSpellcheck=false')

        response = requests.get(search_url, headers=headers).json()
        print(f'Стр. {page}: Cтатус - Завершен!')

        with open(f'./{filename}/data/search_data_{page}.json', 'w', encoding='utf-8') as file:
            json.dump(response, file, ensure_ascii=False, indent=4) # на всякий случай сохраняем все API-шки


def get_products_list():

    files = os.listdir(f'./{filename}/data') # создаем список полученных файлов json
    products_list = [] # здесь будем хранить данные к записи в результирующий файл

    for file in files:
        with open (f'./{filename}/data/{file}', 'r', encoding='utf-8') as file:
            data = json.load(file)

        data = data['data']['products'] # обрезаем ненужные данные с файлов. Берем только данные о товарах.

        for product in data:
            products_list.append(
                {
                    'наименование': product['name'],
                    'артикул для поиска на WB': product['id'],
                    'каталог': product['entity'],
                    'бренд': product['brand'],
                    'поставщик': product['supplier'],
                    'цена без скидки': product['sizes'][0]['price']['basic']/100,
                    'цена со скидкой': product['sizes'][0]['price']['total']/100,
                    'url': 'https://www.wildberries.ru/catalog/%s/detail.aspx' % product['id']
                }

            )

    return products_list


def save_excel(products, filename): # сохраняем полученные данные в файле формата .xlsx

    df = pd.DataFrame(products)

    with pd.ExcelWriter(f'./{filename}/{filename}.xlsx', engine='xlsxwriter') as writer:
        df.to_excel(writer, sheet_name='data', index=False)
        worksheet = writer.sheets['data']
        worksheet.set_column('A:A', 70)  # "наименование"
        worksheet.set_column('B:B', 20)  # "артикул для поиска на WB"
        worksheet.set_column('C:C', 20)  # "каталог"
        worksheet.set_column('D:D', 10)  # "бренд"
        worksheet.set_column('E:E', 10)  # "поставщик"
        worksheet.set_column('F:F', 10)  # "цена без скидки"
        worksheet.set_column('G:G', 10)  # "цена со скидкой"
        worksheet.set_column('H:H', 60)  # "url"

        print("Файл успешно сохранен")


if __name__ == '__main__':
    os.mkdir(f'{filename}')
    os.mkdir(f'./{filename}/data')
    parser(encode_search_data)
    products = get_products_list()
    save_excel(products, filename)


