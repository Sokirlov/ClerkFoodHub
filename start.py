import os
import sys
import time
import datetime
import subprocess
import django

django.setup()

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ClerkFoodhub.settings")
sys.path.insert(0, os.getcwd())

from django.core.management import call_command
from django.contrib.auth import get_user_model

# def get_user():
#     while True:
#         try:
#             uuser = get_user_model()
#             return uusersite_settings_district
#         except:
#             time.sleep(10)
User = get_user_model()


def _vait_time(t):
    for i in range(t):
        print(t-i)


def create_main_user():
    try:
        USER = os.getenv('ADM_USER')
    except NameError:
        print('Environment variable "USER" not found\nSet as default variable "root".')
        USER = 'root'

    try:
        PASS = os.getenv('ADM_PASS')
    except NameError:
        print('Environment variable "PASS" not found\nSet as default variable "root".')
        PASS = 'root'
    User.objects.create_superuser(USER, 'admin@myproject.com', PASS)

def update_caterings():
    try:
        from catering.models import Food, CategoryFood, Provider
        oldfood = Food.objects.filter(category__provider__title='Imperial Food',
                                      date_add__lte=(datetime.datetime.now() - datetime.timedelta(days=10)))
        imperial_all = Food.objects.filter(category__provider__title='Imperial Food')
        if len(imperial_all) == 0 or len(oldfood) > 0:
            print('Треба оновити данні кетерінгів')
            call_command("imperial-food")
        else:
            print('Данні з кетерінгів знадені')
    except ImportError:
        exit('Помилка бази данних')

def run_django():
    print('Усе готово до запуску')
    # call_command("runserver", "0.0.0.0:8008")
    # subprocess.run("gunicorn --workers 3 --timeout 1000 --bind :8008 ClerkFoodhub.wsgi:application")


def add_users():
    try:
        demo = os.getenv('LOAD_DEMO_DATA')
        if demo:
            call_command('loaddata', 'users')
            call_command('loaddata', 'cart')
            print('Демо данні користуачів та корзини були успішно завнатажені')
        else:
            create_main_user()
    except NameError:
        create_main_user()

def add_default_settings():
    try:
        from site_settings.models import District
        if len(District.objects.all()) == 0:
            print('Не знадено районів у базі данних -> Спробуємо завантажити райони')
            call_command('loaddata', 'site_settings')
        else:
            print('Всі райони знаййдено. Можемо продовжувати')
    except Exception as ex:
        print(f'Помилка району {ex}')
        call_command('makemigrations', 'site_settings')
        call_command('migrate', 'site_settings', interactive=False)
        call_command('loaddata', 'site_settings')

def first_start():
    call_command('makemigrations', interactive=False)
    call_command("migrate", interactive=False)
    add_default_settings()
    update_caterings()
    add_users()
    run_django()


def non_first_start(allUsers):
    if len(allUsers) > 0:
        update_caterings()
        _vait_time(5)
        run_django()
    else:
        update_caterings()
        add_users()
        run_django()

def start():
    # validate database
    try:
        from users.models import CustomUser
        non_first_start(CustomUser.objects.all())
    except Exception as ex:
        print(f'Перший запуск! Помилка {ex}')
        first_start()
        # call_command('makemigrations', interactive=False)
        # call_command("migrate", interactive=False)


if __name__ == '__main__':
    start()
    # counter: int = 0
    # while True:
    #     try:
    #         start()
    #         break
    #     except Exception as exc:
    #         if counter == 10:
    #             exit('More 10 try`s')
    #         else:
    #             counter += 1
    #             print(f'Exceptions - {exc}')
    #             time.sleep(10)
