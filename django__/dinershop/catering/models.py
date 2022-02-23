from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from django.utils.safestring import mark_safe


# --- ------------------ It`s model of providers food to collect food by providers
class Provider(models.Model):
    title = models.CharField('Название поставщика', max_length=200)
    link = models.URLField('Ссылка на поставщика')
    id_sort = models.PositiveSmallIntegerField('Порядок сортировки', default=0)
    date_add = models.DateField(auto_now_add=True)

    class Meta:
        ordering = ['id_sort']
        verbose_name = 'Поставщик'
        verbose_name_plural = 'Поставщики'

    def __str__(self):
        return f"{self.title}"


# --- ------------------ It`s model of category food by providers
# --- provider, title, identic, link, id_sort, (date_add)
class CategoryFood(models.Model):
    provider = models.ForeignKey(Provider, verbose_name='Поставщик', on_delete=models.DO_NOTHING)
    title = models.CharField('Категория еды', max_length=200)
    identic = models.CharField('Идентификатор', max_length=300, null=True, blank=True)
    link = models.URLField('Ссылка на кат. товаров', null=True, blank=True)
    id_sort = models.PositiveSmallIntegerField('Порядок сортировки категорий', default=0)
    date_add = models.DateField(auto_now_add=True)

    class Meta:
        ordering = ['id_sort']
        verbose_name = 'Категория товаров'
        verbose_name_plural = 'Категории товаров'

    def __str__(self):
        return f"{self.title}"


# --- ------------------ It`s model of food by category
# ---- category, title, description, price, buy_link, image, link, id_sort, is_active, date_add, last_update
class Food(models.Model):
    category = models.ForeignKey(CategoryFood, verbose_name='Категория еды', on_delete=models.DO_NOTHING)
    title = models.CharField('Название еды', max_length=200)
    description = models.TextField(null=True, blank=True)
    price = models.DecimalField('Цена', max_digits=6, decimal_places=2)
    buy_link = models.CharField('ссылка добавление\nтовара в корзину', max_length=300, null=True, blank=True)
    image = models.CharField('Картинка', max_length=300, null=True, blank=True)
    link = models.URLField('Ссылка на товар', null=True, blank=True)
    id_sort = models.PositiveSmallIntegerField('Порядок сортировки еды', default=0)
    is_active = models.BooleanField('Активен или нет', default=True, help_text='Когда товар неактивен его нельзя заказать. Значит снят с производства.')
    date_add = models.DateField(auto_now_add=True)
    last_update = models.DateField(auto_now=True)

    def food_image_tag(self):
        return mark_safe(f'<img src="{self.image}" width="50" />')

    food_image_tag.short_description = 'Фото'

    class Meta:
        ordering = ['id_sort', 'title']
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    def __str__(self):
        return f"{self.title}"



# -----------  data_add, user, food, quantity, order_for_day, payer
class Orders(models.Model):
    data_add = models.DateField(auto_now_add=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Кто заказывал', related_name='client')
    food = models.ManyToManyField(Food, verbose_name='Блюдо')#, on_delete=models.DO_NOTHING, verbose_name='Блюдо')
    quantity = models.PositiveSmallIntegerField('Количество', default=0)
    order_for_day = models.DateField('Заказ на дату')
    payer = models.ForeignKey(User, blank=True, null=True, on_delete=models.DO_NOTHING, verbose_name='Плтельщик', related_name='payer')

    class Meta:
        ordering = ['-order_for_day', '-data_add']
        verbose_name = 'Заказ'
        verbose_name_plural ='Заказы'


    def __str__(self):
        return f'{self.order_for_day} {self.user}'

