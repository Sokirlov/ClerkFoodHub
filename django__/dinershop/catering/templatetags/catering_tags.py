import re
import locale
import calendar
import datetime
from datetime import timedelta
from django import template
register = template.Library()

today = datetime.datetime.now()


@register.filter(name='wekdays')
def wekdays(append):
    # locale.getlocale()
    # locale.setlocale(locale.LC_ALL, ('ru_RU', 'UTF-8'))
    nextday = today + datetime.timedelta(days=int(append))
    local_cal = calendar.LocaleHTMLCalendar(locale='Russian_Russia')
    header_weekday = local_cal.formatweekday(nextday.weekday())
    weekday = re.match(r'.+>(\w+)<.+', header_weekday)
    # long_dayname = calendar.day_name[nextday.weekday()]
    if weekday:
        return weekday[1]
    else:
        return 0

@register.filter(name='nextdays')
def nextdays(append):
    day = today + timedelta(days=append)
    return datetime.datetime.strftime(day, '%d/%m/%Y %H:%m')