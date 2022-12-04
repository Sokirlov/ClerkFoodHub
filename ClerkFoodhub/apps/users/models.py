import re
from django.db import models
from django.utils.safestring import mark_safe
from django.contrib.auth.models import AbstractUser

from site_settings.models import District
# from django.contrib.auth.admin import UserAdmin

class Company(models.Model):
    title = models.CharField('Назва компанії', max_length=500)
    district = models.ForeignKey(District, verbose_name='Обслуговування', on_delete=models.CASCADE, default=0)
    adress = models.CharField('Адреса', max_length=500, null=True, blank=True, help_text='(Поки що чисто для статистики. Моливо будемо автоматично форму заповняти)')
    # superuser = models.ForeignKey(Worker, verbose_name='Супер користувач', on_delete=models.DO_NOTHING)
    # date_add = models.DateTimeField('Дата створення', auto_now_add=True)
    class Meta:
        ordering = ['title']
        verbose_name = 'Компанія'
        verbose_name_plural = '1. Компанії'

    def __str__(self):
        return f"{self.title}"


class Departament(models.Model):
    company = models.ForeignKey(Company, verbose_name='Назва Компанії', on_delete=models.CASCADE, related_name='organization')
    title = models.CharField('Відділ', max_length=500)
    date_add = models.DateTimeField('Дата створення', auto_now_add=True)
    ordering = models.PositiveSmallIntegerField('Сортування', default=0)

    class Meta:
        ordering = ['ordering']
        verbose_name = 'Відділ'
        verbose_name_plural = '2. Відділи'

    def __str__(self):
        return f"{self.title} ({self.company})"



class CustomUser(AbstractUser):
    departament = models.ForeignKey(Departament, verbose_name='Відділ', on_delete=models.CASCADE, related_name='departament', null=True, blank=True)
    job_title = models.CharField('Посада', max_length=500, null=True, blank=True)
    phone = models.CharField('Телефон', max_length=20, null=True, blank=True)
    avatar = models.ImageField('', null=True, blank=True)
    # date_add = models.DateTimeField('Дата створення', auto_now_add=True)
    ordering = models.PositiveSmallIntegerField('Сортування', default=0)

    def avatar_image_tag(self):
        return mark_safe(f'<img src="/media/{self.avatar}" width="50" />')
    avatar_image_tag.short_description = 'Світлина'

    def save(self, *args, **kwargs):
        print(self.__dict__)
        if self.phone:
            ph_arr = re.findall('\d', self.phone)
            self.phone = str().join(ph_arr)
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['departament', 'ordering']
        verbose_name = 'Співробітник'
        verbose_name_plural = '2. Співробітники'

    # def __str__(self):
    #     return f"{self.first_name +' '+ self.last_name}"
