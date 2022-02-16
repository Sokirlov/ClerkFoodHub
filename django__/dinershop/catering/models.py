from django.db import models



# --- ------------------ It`s model of providers food to collect food by providers
class Provider(models.Model):
    title = models.CharField('Название поставщика', max_length=200)
    link = models.URLField('Ссылка на поставщика')
    id_sort = models.PositiveSmallIntegerField('Порядок сортировки', default=0)
    date_add = models.DateField(auto_now_add=True)

    class Meta:
        ordering = ['id_sort']
        verbose_name = 'Поставщики'

    def __str__(self):
        return f"{self.title}"