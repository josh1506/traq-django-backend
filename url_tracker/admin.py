from django.contrib import admin
from .models import Url, Viewer
# Register your models here.


@admin.register(Url)
class UrlAdmin(admin.ModelAdmin):
    list_display = ('title', 'link', 'total_visitors')
    search_fields = ('title', 'link')


@admin.register(Viewer)
class ViewerAdmin(admin.ModelAdmin):
    list_display = ('url', 'date_viewed')
