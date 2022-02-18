from django.db import models


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
class Food(models.Model):
    provider = models.ForeignKey(CategoryFood, verbose_name='Категория еды', on_delete=models.DO_NOTHING)
    title = models.CharField('Название еды', max_length=200)
    description = models.TextField(null=True, blank=True)
    price = models.DecimalField('Цена', max_digits=6, decimal_places=2)
    buy_link = models.CharField('ссылка добавление\nтовара в корзину', max_length=300, null=True, blank=True)
    identic = models.CharField('Идентификатор', max_length=300, null=True, blank=True)
    link = models.URLField('Ссылка на товар', null=True, blank=True)
    id_sort = models.PositiveSmallIntegerField('Порядок сортировки еды', default=0)
    is_active = models.BooleanField('Активен или нет', default=True, help_text='Когда товар неактивен его нельзя заказать. Значит снят с производства.')
    date_add = models.DateField(auto_now_add=True)
    last_update = models.DateField(auto_now=True)

    class Meta:
        ordering = ['id_sort']
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    def __str__(self):
        return f"{self.title}"
