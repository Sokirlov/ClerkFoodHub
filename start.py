import os, sys, time
import subprocess
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ClerkFoodhub.settings")
sys.path.insert(0, os.getcwd())
import django
from django.core.management import call_command
django.setup()
from django.contrib.auth import get_user_model
User = get_user_model()

USER = os.getenv('ADM_USER')
PASS = os.getenv('ADM_PASS')



def start():
    try:
        # from users.models import CustomUser
        if len(User.objects.all()) >= 1:
            call_command("runserver", "0.0.0.0:8000")
        else:
            print('----- ITS else work\n\n\n')
            call_command("migrate", interactive=False)
            User.objects.create_superuser(USER, 'admin@myproject.com', PASS)
            call_command("imperial-food")
            print('food is parsed well')
            call_command("runserver", "0.0.0.0:8000")
            # from django.contrib.auth import get_user_model
            # User = get_user_model()
            # subprocess.run(f"python manage.py createsuperuser && {USER} &&  && {PASS} && {PASS} && y")
            # subprocess.run("python manage.py runserver 0.0.0.0:8000")
    except:
        print('!!!!!!! EXCEPTION work\n\n\n')
        call_command("migrate", interactive=False)
        User.objects.create_superuser(USER, 'admin@myproject.com', PASS)
        call_command("runserver", "0.0.0.0:8000")

if __name__=='__main__':
    while True:
        try:
            start()
            break
        except:
            time.sleep(10)