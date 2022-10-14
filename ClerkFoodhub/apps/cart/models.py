from django.db import models
from users.models import CustomUser
from catering.models import Food, Provider



class Orders(models.Model):
    """
    "data_add", "user", "catering", "food", "quantity", "order_for_day", "payer", "provider_cart_id",
    """
    data_add = models.DateField(auto_now_add=True)
    user = models.ForeignKey(CustomUser, on_delete=models.DO_NOTHING, verbose_name='Замовляв', related_name='user')
    catering = models.ForeignKey(Provider, verbose_name='Кейтерінг', on_delete=models.DO_NOTHING, related_name='catering')
    food = models.ForeignKey(Food, verbose_name='Страва', on_delete=models.DO_NOTHING, related_name='food')
    quantity = models.PositiveSmallIntegerField('Кількість', default=1)
    order_for_day = models.DateField('На яку дату замовлення')
    payer = models.ForeignKey(CustomUser, blank=True, null=True, on_delete=models.DO_NOTHING, verbose_name='Оплатив', related_name='payer')
    provider_cart_id = models.CharField('Номер замовлення у кейтерінгу', blank=True, null=True, max_length=50)

    class Meta:
        ordering = ['-order_for_day', '-user']
        verbose_name = 'Замовлення'
        verbose_name_plural ='Замовлення'

    def __str__(self):
        return f'{self.order_for_day} {self.user}'