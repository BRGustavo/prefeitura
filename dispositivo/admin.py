from django.contrib import admin
from .models import Roteador


class RoteadorModel(admin.ModelAdmin):
    list_display = ['id', 'ssid', 'senha', 'modelo', 'multimodo', 'departamento']
    list_display_links = ['ssid']
    list_editable = ['multimodo']

admin.site.register(Roteador, RoteadorModel)