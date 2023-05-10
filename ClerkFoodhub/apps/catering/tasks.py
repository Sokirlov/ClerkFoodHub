from django.core import management
from celery import shared_task



CATERING_LIST = ['imperial-food',]

@shared_task
def call_update(catering):
    management.call_command(catering)
    return True

@shared_task
def week_update_catering():
    for food in CATERING_LIST:
        call_update.delay(food)
    return True