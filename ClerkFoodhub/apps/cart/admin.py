import datetime
from django.contrib import admin
from cart.models import Orders
from users.models import CustomUser


def delete_payer(self, request, queryset, **kwargs):
    queryset.update(payer=None)
delete_payer.short_description = "Прибрати оплату"

def change_order_day_on_one_week_forward(self, request, queryset, **kwargs):
    for i in queryset:
        new_date = i.order_for_day + datetime.timedelta(days=7)
        i.order_for_day=new_date
        i.save()
    # queryset.update(payer=None)
change_order_day_on_one_week_forward.short_description = "Перенести замовлення на тиждень вперед"

def change_order_day_on_one_week_backward(self, request, queryset, **kwargs):
    for i in queryset:
        new_date = i.order_for_day - datetime.timedelta(days=7)
        i.order_for_day=new_date
        i.save()
    # queryset.update(payer=None)
change_order_day_on_one_week_backward.short_description = "Перенести замовлення на тиждень назад"


@admin.register(Orders)
class ProviderAdmin(admin.ModelAdmin):
    list_display = ["data_add", "user", "catering", "food", "food_price", "quantity", "order_for_day", "payer", "provider_cart_id"]
    readonly_fields = ('sum_spliwise',)
    list_filter = ["user", "order_for_day", "payer"]
    actions = [delete_payer, change_order_day_on_one_week_forward, change_order_day_on_one_week_backward]
    fieldsets = (
        ('Замовлення', {'fields': ("user", "catering", "food", "quantity", "order_for_day", "payer", "provider_cart_id", "sum_spliwise",)}),
    )

    @admin.display(description='Ціна')
    def food_price(self, obj):
        return obj.food.price
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if not request.user.is_superuser:
            qs = qs.filter(user=request.user)
        return qs
    def formfield_for_foreignkey(self, db_field, request, **kwargs):

        if not request.user.is_superuser:
            if db_field.name == "user" or db_field.name == "payer":
                kwargs["queryset"] = CustomUser.objects.filter(departament=request.user.departament)
            return super().formfield_for_foreignkey(db_field, request, **kwargs)
        else:
            return super().formfield_for_foreignkey(db_field, request, **kwargs)