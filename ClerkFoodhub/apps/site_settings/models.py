from django.db import models


class City(models.Model):
    title = models.CharField('Назва міста', max_length=50)
    ordering = models.PositiveSmallIntegerField('Сортування', default=0)
    date_add = models.DateTimeField('Дата додавання', auto_now_add=True)

    class Meta:
        ordering = ['ordering']
        verbose_name = 'Місто'
        verbose_name_plural = '1. Міста'

    def __str__(self):
        return f"{self.title}"

class Region(models.Model):
    city = models.ForeignKey(City, verbose_name='Місто', on_delete=models.DO_NOTHING)
    title = models.CharField('Частина міста', max_length=50)
    ordering = models.PositiveSmallIntegerField('Сортування', default=0)
    date_add = models.DateTimeField('Дата додавання', auto_now_add=True)

    class Meta:
        ordering = ['ordering']
        verbose_name = 'Частину міста'
        verbose_name_plural = '2. Частини міста'

    def __str__(self):
        return f"{self.title}"


class District(models.Model):
    region = models.ForeignKey(Region, verbose_name='Місто', on_delete=models.DO_NOTHING)
    title = models.CharField('Назва району', max_length=50)
    ordering = models.PositiveSmallIntegerField('Сортування', default=0)
    date_add = models.DateTimeField('Дата додавання', auto_now_add=True)

    class Meta:
        ordering = ['ordering']
        verbose_name = 'Район'
        verbose_name_plural = '3. Райони'

    def __str__(self):
        return f"{self.title}"