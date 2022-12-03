import os, sys
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
            call_command("migrate", interactive=False)
            # from django.contrib.auth import get_user_model
            # User = get_user_model()
            User.objects.create_superuser(USER, 'admin@myproject.com', PASS)
            # subprocess.run(f"python manage.py createsuperuser && {USER} &&  && {PASS} && {PASS} && y")
            call_command("runserver", "0.0.0.0:8000")
            # subprocess.run("python manage.py runserver 0.0.0.0:8000")
    except:

        call_command("migrate", interactive=False)
        User.objects.create_superuser(USER, 'admin@myproject.com', PASS)
        call_command("runserver", "0.0.0.0:8000")

if __name__=='__main__':
    start()