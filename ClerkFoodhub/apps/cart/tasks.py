from celery import shared_task
from .models import Orders
import datetime

@shared_task
def update_cart_data():
    today = datetime.datetime.now()
    queryset = Orders.objects.filter(order_for_day__lte=today)
    for i in queryset:
        new_date = i.order_for_day + datetime.timedelta(days=7)
        i.order_for_day = new_date
        i.payer = None
        i.save()
    return True