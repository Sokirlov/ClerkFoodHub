from django.contrib import admin
from cart.models import Orders

# Register your models here.
@admin.register(Orders)
class ProviderAdmin(admin.ModelAdmin):
    pass