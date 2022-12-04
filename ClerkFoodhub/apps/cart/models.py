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

    def sum_credits_by_payer(self, orders):
        print('credit')
        payments = {}
        for ord in orders:
            try:
                print(f'{ord.payer.first_name} {ord.payer.last_name}')
                payments[ord.payer.username] += ord.food.price * ord.quantity
            except KeyError:
                print('except')
                payments[ord.payer.username] = ord.food.price * ord.quantity
        return payments
    def sum_debits_by_payer(self, orders):
        print('Debit')
        payments = {}
        for ord in orders:
            try:
                payments[ord.user.username] += ord.food.price * ord.quantity
            except KeyError:
                payments[ord.user.username] = ord.food.price * ord.quantity
        return payments
    def sum_spliwise(self):
        all_orders = Orders.objects.filter(user=self.user)
        all_credits = self.sum_credits_by_payer(Orders.objects.filter(user=self.user).exclude(payer=self.user))
        print('summ')
        all_debits = self.sum_debits_by_payer(Orders.objects.filter(payer=self.user).exclude(user=self.user))
        print(all_orders)
        splitw = all_credits
        splitw.update((a, b*-1) for a, b in splitw.items())
        for deb, s in all_debits.items():
            try:
                splitw[deb] = s + all_credits[deb]
            except KeyError:
                splitw[deb] = s
        return splitw

    class Meta:
        ordering = ['-order_for_day', '-user']
        verbose_name = 'Замовлення'
        verbose_name_plural ='Замовлення'

    def __str__(self):
        return f'{self.order_for_day} {self.user}'