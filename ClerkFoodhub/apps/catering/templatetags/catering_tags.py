import sys
import re
import locale
import calendar
from babel.dates import format_datetime
import datetime
from datetime import timedelta
from django import template
register = template.Library()

today = datetime.datetime.now()


@register.filter(name='wekdays')
def wekdays(append):
    # locale.getlocale()
    # locale.setlocale(locale.LC_ALL, ('uk_UA', 'UTF-8'))
    if sys.platform == 'win32':
        locale.setlocale(locale.LC_ALL, 'ukr_ukr')
    else:
        locale.setlocale(locale.LC_ALL, 'uk_UA.UTF-8')
    day = today + timedelta(days=append)
    return datetime.datetime.strftime(day, '%a %e')

@register.filter(name='nextdays')
def nextdays(append):
    day = today + timedelta(days=append)
    return datetime.datetime.strftime(day, '%d/%m/%Y %H:%m')

