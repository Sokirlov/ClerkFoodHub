import datetime, calendar
from datetime import timedelta
from django import template
register = template.Library()
today = datetime.datetime.now()

@register.filter(name='wekdays')
def wekdays(append):
    nextday = today + timedelta(days=append)
    long_dayname = calendar.day_name[nextday.weekday()]
    return long_dayname[:2]