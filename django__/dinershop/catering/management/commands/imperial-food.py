from django.core.management.base import BaseCommand
from catering.models import Provider, CategoryFood, Food
import requests
from bs4 import BeautifulSoup
import datetime


provider = Provider.objects.get(link='https://food.imperialcatering.com.ua/')
category = {}


class Dishes:
    def get_tabs_data(self, soup):

        menu_tab = soup.find('ul', id="mondayTab")
        all_button = menu_tab.find_all('a')
        for i in all_button:
            title = i.text.strip()
            identic = i['href'][1:]
            try:
                CategoryFood.objects.get(provider=provider, title=title)
            except:
                # --- provider, title, identic, link, id_sort, (date_add)
                CategoryFood.objects.create(provider=provider, title=title, identic=identic)
            tab_key = i['href'][1:]
            category[tab_key] = i.text.strip()
        return category


    def pars_data(self, response=None):
        if response:
            soup = BeautifulSoup(response.text, 'html.parser')
        else:
            pass

        tab_dict = self.get_tabs_data(self, soup)
        print(tab_dict)
        # for cat, name in tab_dict.items():
        #     prodcut.append(name)
        #     pars_food(soup, cat)


    def get_pages():
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
        response = requests.session().get('https://food.imperialcatering.com.ua/', headers=headers)
        if response.status_code == 200:
            print("In Work with ")
            return response
        else:
            print("Bad result")


    def __init__(self, *args, **kwargs):
        return self.__dict__.update(kwargs)



class Command(BaseCommand):
    def handle(self, *args, **options):
        page = Dishes.get_pages()
        Dishes.pars_data(Dishes, page)


# if __name__ == '__main__':
#     page = Dishes.get_pages()
#     Dishes.pars_data(Dishes, page)
