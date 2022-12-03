from django.contrib import admin
from cart.models import Orders
from users.models import CustomUser

# Register your models here.
@admin.register(Orders)
class ProviderAdmin(admin.ModelAdmin):
    list_display = ["data_add", "user", "catering", "food", "food_price", "quantity", "order_for_day", "payer", "provider_cart_id"]

    readonly_fields = ('sum_spliwise',)
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