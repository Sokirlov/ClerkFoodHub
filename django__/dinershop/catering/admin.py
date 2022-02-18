from django.contrib import admin
from .models import Provider, CategoryFood, Food

# Register your models here.
# @admin.register(Author)
# class AuthorAdmin(admin.ModelAdmin):


@admin.register(Provider, CategoryFood, Food)
class ProviderAdmin(admin.ModelAdmin):
    pass
    # list_display = ['']

# @admin.register(CategoryFood)
# class CategoryFoodAdmin(admin.ModelAdmin):
#
#
# @admin.register(Food)
# class FoodFoodAdmin(admin.ModelAdmin):