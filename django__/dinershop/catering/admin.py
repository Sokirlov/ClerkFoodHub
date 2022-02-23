from django.contrib import admin
from catering.models import Provider, CategoryFood, Food, Orders

# Register your models here.
# @admin.register(Author)
# class AuthorAdmin(admin.ModelAdmin):


@admin.register(Provider)
class ProviderAdmin(admin.ModelAdmin):
    pass
    # list_display = ['']

# @admin.register(CategoryFood)
# class CategoryFoodAdmin(admin.ModelAdmin):
#
#
# @admin.register(Food)
# class FoodFoodAdmin(admin.ModelAdmin):
@admin.register(Orders)
# -----------  data_add, user, food, quantity, order_for_day, payer
class OrdersAdmin(admin.ModelAdmin):
    list_display = ['order_for_day', 'user', 'payer']
    # search_fields = ['food', ]
    # autocomplete_fields = ['food']


@admin.register(Food)
# ---- category, title, description, price, buy_link, image, link, id_sort, is_active, date_add, last_update
class FoodAdmin(admin.ModelAdmin):
    list_display = ['id', 'food_image_tag', 'title', 'price', 'category', 'is_active', 'date_add', 'last_update']
    list_filter = ['category', 'is_active',]
    readonly_fields = ['food_image_tag', ]

@admin.register(CategoryFood)
# --- provider, title, identic, link, id_sort, (date_add)
class CategoryFoodAdmin(admin.ModelAdmin):
    list_display = ['title', 'identic', 'id_sort', 'link',]
    list_editable = ['id_sort',]
    list_filter = ['provider',]