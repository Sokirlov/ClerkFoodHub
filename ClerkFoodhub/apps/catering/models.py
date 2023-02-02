from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from django.utils.safestring import mark_safe
from site_settings.models import District
# from clients.models import Worker



# --- ------------------ It`s model of providers food to collect food by providers
class Provider(models.Model):
    """
        "title", "link", "id_sort", "date_add", "min_order", "district",
    """
    title = models.CharField('Назва кейтерінгу', max_length=200)
    link = models.URLField('Посилання')
    id_sort = models.PositiveSmallIntegerField('Сортування', default=0)
    date_add = models.DateField(auto_now_add=True)
    min_order = models.PositiveSmallIntegerField('Мінімальне замовлення', default=0)
    district = models.ManyToManyField(District, verbose_name='Обслуговування', blank=True)

    class Meta:
        ordering = ['id_sort']
        verbose_name = 'Кейтерінг'
        verbose_name_plural = '1. Перелік Кейтерінгів'

    def __str__(self):
        return f"{self.title}"


# --- ------------------ It`s model of category food by providers
# --- provider, title, identic, link, id_sort, (date_add)
class CategoryFood(models.Model):
    """
    "provider", "title", "identic", "link", "id_sort", "date_add"
    """

    provider = models.ForeignKey(Provider, verbose_name='Кейтерінг', related_name='categorysfoods', on_delete=models.DO_NOTHING )
    title = models.CharField('Категорія страви', max_length=200)
    identic = models.CharField('ID категорії', max_length=300, null=True, blank=True)
    link = models.URLField('Посилання  категорії', null=True, blank=True)
    id_sort = models.PositiveSmallIntegerField('Сортування', default=0)
    date_add = models.DateField(auto_now_add=True)

    class Meta:
        ordering = ['id_sort']
        verbose_name = 'Категорія страв'
        verbose_name_plural = '2. Категорії страв'

    def __str__(self):
        return f"{self.title}"



class Food(models.Model):
    """
    It`s model of food by category
    "category", "title", "description", "price", "buy_link", "image", "link", "id_sort", "is_active", "date_add", "last_update"

    """
    ##TODO  Get from caterig waight of food
    category = models.ForeignKey(CategoryFood, on_delete=models.DO_NOTHING, related_name='foods', verbose_name='Категорія страви')
    title = models.CharField('Страва', max_length=200)
    description = models.TextField('Інгрідієнти', null=True, blank=True)
    weight = models.CharField('Вага', max_length=10, null=True, blank=True, default=0)
    price = models.DecimalField('Ціна', max_digits=6, decimal_places=2)
    buy_link = models.CharField('Посилання на додавання\nУ кошик', max_length=300, null=True, blank=True)
    image = models.CharField('Світлина', max_length=300, null=True, blank=True)
    link = models.CharField('Посилання на сторінку товара', max_length=300, null=True, blank=True)
    id_sort = models.PositiveSmallIntegerField('Сортування', default=0)
    is_active = models.BooleanField('Увімк / Вимк', default=True, help_text='Когда товар неактивен его нельзя заказать. Значит снят с производства.')
    date_add = models.DateField('Дата додавання', auto_now_add=True)
    last_update = models.DateField('Дата оновлення', auto_now=True)

    def food_image_tag(self):
        return mark_safe(f'<img src="{self.image}" width="50" />')

    food_image_tag.short_description = 'Фото'

    class Meta:
        ordering = ['id_sort', 'title']
        verbose_name = 'Страва'
        verbose_name_plural = '3. Страви'

    def __str__(self):
        return f"{self.title}"
