import time

import requests
from bs4 import BeautifulSoup
import httplib2
import apiclient.discovery
from oauth2client.service_account import ServiceAccountCredentials
import datetime
import json
import re

today = datetime.date.today()

class Prodcut:
    image = str
    title = str
    link = str
    descr = str
    price = str

    def __init__(self, image, title, link, descr, price):
        self.image = image
        self.title = title
        self.link = link
        self.descr = descr
        self.price = price

    def __repr__(self):
        return str(self.__dict__)

prodcut = []


def write_to_excel(obj):
    values =obj
    print(obj)
    CREDENTIALS_FILE = 'parser-data-flats-in-kyiv-65ba53896b5d.json'  # Имя файла с закрытым ключом, вы должны подставить свое

    # Читаем ключи из файла
    credentials = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_FILE,
                                                                   ['https://www.googleapis.com/auth/spreadsheets',
                                                                    'https://www.googleapis.com/auth/drive'])
    httpAuth = credentials.authorize(httplib2.Http())  # Авторизуемся в системе
    spreadsheetId = '1_vMbXDjj7Rg85RTQfJ0xLNncsxMGO2547cMmbnig68I'

    service = apiclient.discovery.build('sheets', 'v4', http=httpAuth)  # Выбираем работу с таблицами и 4 версию API
    # results = service.spreadsheets().values().append(
    results = service.spreadsheets().values().batchUpdate(
        spreadsheetId=spreadsheetId,
        body={
            "valueInputOption": "USER_ENTERED",
            "requests": [
                {
                    "appendDimension": {
                        "sheetId": 'МЕНЮ2',
                        "dimension": "ROWS",
                        "length": 13
                    }
                }
            ],
            "data": [{
                "range": 'МЕНЮ2!A4:E1000',
                "majorDimension": "ROWS",
                "values": values,
            }]
        }).execute()
categorus = {}

def get_tabs_data(soup):
    menu_tab = soup.find('ul', id="mondayTab")
    all_button = menu_tab.find_all('a')
    for i in all_button:
         tab_key = i['href'][1:]
         categorus[tab_key] = [i.text.strip()]
    return categorus

def pars_food(soup, cat):
    blcok_food = soup.find('div', id=cat)
    for rows in blcok_food.find_all('li', class_='dish-item'):
        image = rows.find('img')['data-original']
        link = rows.find('a', class_='addtocart')['href']  # .replace('/component/jshopping/cart/add.html?', '')
        title = re.sub("\"", "", rows.find('h3').text.strip())
        descr = rows.find('p', class_="dish-consist").text.strip()
        price = re.sub(" грн", "", rows.find('p', class_="dish-price").text.strip())
        data = [f'=IMAGE("{image}";1)', f'{title}', f'{descr}', f'{price}',
                f'https://food.imperialcatering.com.ua{link}']
        prodcut.append(data)


def olx_pars_data(response):
    soup = BeautifulSoup(response.text, 'html.parser')
    if soup.text.find('Не найдено ни одного объявления') > 0:
        print("Нет результата")
        pass
    else:
        tab_dict = get_tabs_data(soup)
        for cat, name in tab_dict.items():
            prodcut.append(name)
            pars_food(soup, cat)



        # for rows in soup.find_all('li', class_='dish-item'):
        #     image = rows.find('img')['data-original']
        #     link = rows.find('a', class_='addtocart')['href']#.replace('/component/jshopping/cart/add.html?', '')
        #     title = re.sub("\"", "", rows.find('h3').text.strip())
        #     descr = rows.find('p', class_="dish-consist").text.strip()
        #     price = re.sub(" грн", "", rows.find('p', class_="dish-price").text.strip())
        #     data = [f'=IMAGE("{image}";1)', f'{title}', f'{descr}', f'{price}', f'https://food.imperialcatering.com.ua{link}']
        #     prodcut.append(data)
        write_to_excel(prodcut)




def get_datas(searched_url, headers):
    response = session.get(searched_url, headers=headers)
    if response.status_code == 200:
        print("In Work with ")
        return response
    else:
        print("Bad result")


session = requests.session()

headers = {
    'authority': 'www.kith.com',
    'cache-control': 'max-age=0',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36',
    'accept': '*/*',
    'accept-encoding': 'gzip, deflate, br',
    'sec-fetch-dest': 'document',
    'sec-fetch-site': 'cross-site',
    'sec-fetch-mode': 'no-cors',
    'sec-fetch-user': '?1',
    'accept-language': 'uk-UA,uk;q=0.9',
}

def parse_olx():
    searched_url = 'https://food.imperialcatering.com.ua/'
    response = get_datas(searched_url, headers)
    olx_pars_data(response)

parse_olx()
print("Successful")
