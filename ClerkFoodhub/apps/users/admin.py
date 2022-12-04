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
    list_display = ['id', 'company', 'title', 'ordering']
    list_display_links = ['id', 'title']
    list_editable = ['ordering']

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if not request.user.is_superuser:
            qs = qs.filter(company=request.user.departament.company)
        return qs




# class MyUserChangeForm(UserChangeForm):
#     class Meta:
#         model = get_user_model()
#
# class MyUserCreationForm(UserCreationForm):
#     class Meta:
#         model = get_user_model()
#
# class MyUserAdmin(UserAdmin):
#     form = MyUserChangeForm
#     add_form = MyUserCreationForm

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ['id', 'first_name', 'last_name', 'phone', 'departament', 'departament_organization', 'ordering']
    list_display_links = ['id', 'first_name', 'last_name', 'phone']
    list_editable = ['ordering']
    list_filter = ['departament']
    readonly_fields = ('avatar_image_tag',)
    fieldsets = (
        ('Додатковы iнфа', {'fields': ('departament', 'first_name', 'last_name', 'email', 'phone', ('avatar_image_tag', 'avatar'), 'ordering', 'last_login',)}),
        ('Співробітник',
         {'fields': ('username', 'password',  'date_joined', ('is_active', 'is_staff', 'is_superuser',), 'user_permissions', )}),
    )
    @admin.display(description='Компанія')
    def departament_organization(self, obj):
        try:
            return obj.departament.company
        except AttributeError:
            return '--'

    def get_queryset(self, request):
        print(f'get_queryset {self.__dict__}')
        qs = super().get_queryset(request)
        if not request.user.is_superuser:
            qs = qs.filter(departament__company=request.user.departament.company)
        return qs

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if not request.user.is_superuser:
            if db_field.name == "departament":
                kwargs["queryset"] = Departament.objects.filter(company=request.user.departament.company)
            return super().formfield_for_foreignkey(db_field, request, **kwargs)
        else:
            if db_field.name == "departament":
                all_dep = Departament.objects.all().values_list('company__title', 'title')
                print(f'{all_dep}')
                kwargs["queryset"] = Departament.objects.all()
            return super().formfield_for_foreignkey(db_field, request, **kwargs)

    # def get_fieldsets(self, request, obj=None):
    #     if request.user.is_superuser:
    #         return (('User',{'fields': ('username', 'password',  )}),)
    #     else:
    #         return (('User', {'fields': ('username', 'password', )}),)

admin.site.register(CustomUser, CustomUserAdmin)
