import datetime, calendar
from datetime import timedelta
from django import template
import re
import locale
register = template.Library()
today = datetime.datetime.now()

@register.filter(name='wekdays')
def wekdays(append):
    # locale.getlocale()
    # locale.setlocale(locale.LC_ALL, 'uk.utf8')
    nextday = today + timedelta(days=append)
    local_cal = calendar.LocaleHTMLCalendar(locale='Russian_Russia')
    header_weekday = local_cal.formatweekday(nextday.weekday())
    weekday = re.match(r'.+>(\w+)<.+', header_weekday)
    long_dayname = calendar.day_name[nextday.weekday()]
    return weekday[1]

@register.filter(name='nextdays')
def nextdays(append):
    return today + timedelta(days=append)