import os, sys, time
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ClerkFoodhub.settings")
sys.path.insert(0, os.getcwd())
import django
django.setup()
from django.core.management import call_command
from django.contrib.auth import get_user_model
print('2134')

def get_user():
    while True:
        try:
            uuser = get_user_model()
            return uuser
        except:
            time.sleep(10)
User = get_user()

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
    print('__________It`s new run______')
    call_command("migrate", interactive=False)
    User.objects.create_superuser(USER, 'admin@myproject.com', PASS)

def update_caterings():
    call_command("imperial-food")


def run_django():
    print('All data was updated.\nNow RUN.')
    call_command("runserver", "0.0.0.0:8000")


def load_demo():
    call_command("migrate", interactive=False)
    print('Try load data to DB site_settings')
    call_command('loaddata', 'site_settings')
    print('Try load data to DB users')
    call_command('loaddata', 'users')
    update_caterings()
    print('Try load data to DB cart')
    call_command('loaddata', 'cart')

def start():
    try:
        from users.models import CustomUser
        if len(User.objects.all()) >= 1:
            print(f'User is more 0 now it`s {len(User.objects.all())}')
            update_caterings()
            run_django()
        else:
            if os.getenv('LOAD_DEMO_DATA'):
                print('Try load data to DB')
                load_demo()
                print('Data  will load at DB')
            else:
                create_main_user()
                update_caterings()
    except Exception as ex:
        print(f'Exception is {ex}')
        if os.getenv('LOAD_DEMO_DATA'):
            load_demo()
            print('Data  will load at DB')
        else:
            create_main_user()
            update_caterings()
    finally:
        call_command("runserver", "0.0.0.0:8000")


if __name__ == '__main__':
    counter: int = 0
    while True:
        try:
            start()
            break
        except Exception as exc:
            if counter == 10:
                exit('More 10 try`s')
            else:
                counter += 1
                print(f'Exceptions - {exc}')
                time.sleep(10)
