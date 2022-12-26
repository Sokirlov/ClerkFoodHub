from django.contrib import admin
from site_settings.models import City, Region, District


@admin.register(City)
class ProviderAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'ordering', 'date_add']
    list_display_links = ['id', 'title']
    list_editable = ['ordering']

@admin.register(Region)
class ProviderAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'city', 'ordering', 'date_add']
    list_display_links = ['id', 'title']
    list_editable = ['city', 'ordering']

@admin.register(District)
class ProviderAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'region', 'ordering', 'date_add']
    list_display_links = ['id', 'title']
    list_editable = ['region', 'ordering']
