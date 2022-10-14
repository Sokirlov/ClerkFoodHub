from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser, Company, Departament

@admin.register(Company)
class OrdersAdmin(admin.ModelAdmin):
    list_display = ['id', 'title']
    list_display_links = ['id', 'title']

@admin.register(Departament)
class OrdersAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'ordering']
    list_display_links = ['id', 'title']
    list_editable = ['ordering']

# @admin.register(CustomUser)
# class OrdersAdmin(UserAdmin):
#     list_display = ['id', 'first_name', 'last_name', 'phone', 'departament', 'ordering']
#     list_display_links = ['id', 'first_name', 'last_name', 'phone']
#     list_editable = ['ordering']
#     add_form = CustomUserCreationForm
#     form = CustomUserChangeForm
#



class CustomUserAdmin(UserAdmin):
    # add_form = CustomUserCreationForm
    # form = CustomUserChangeForm

    model = CustomUser
    list_display = ['id', 'first_name', 'last_name', 'phone', 'departament', 'ordering']
    list_display_links = ['id', 'first_name', 'last_name', 'phone']
    list_editable = ['ordering']
    readonly_fields = ('avatar_image_tag',)
    fieldsets = (

        ('Додатковы iнфа', {'fields': ('departament', 'first_name', 'last_name', 'email', 'phone', ('avatar_image_tag', 'avatar'), 'ordering', 'last_login',)}),
        ('Співробітник',
         {'fields': ('username', 'password',  'date_joined', ('is_active', 'is_staff', 'is_superuser',), 'user_permissions', )}),

    )

admin.site.register(CustomUser, CustomUserAdmin)
