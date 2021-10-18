from django.contrib import admin
from .models import (
    Teclado, Monitor, Mouse, PlacaMae,
    Hd, Processador, Gabinete
)

class TecladoModel(admin.ModelAdmin):
    list_display = ['id', 'marca', 'usb', 'funciona']
    list_display_links = ['id', 'marca']
    list_editable = ['funciona']

class MouseModel(admin.ModelAdmin):
    list_display = ['id', 'marca', 'usb', 'funciona']
    list_display_links = ['id', 'marca']
    list_editable = ['funciona']

class MonitorModel(admin.ModelAdmin):
    list_display = ['id', 'marca', 'hdmi', 'tamanho', 'funciona']
    list_display_links = ['id', 'marca']
    list_editable = ['funciona']

class PlacaMaeModel(admin.ModelAdmin):
    list_display = ['id', 'marca', 'modelo', 'hdmi', 'suporte','processador', 'funciona']
    list_display_links = ['id', 'marca', 'modelo']

    def suporte(self, object):
       return object.processador_suporte
    
    def processador(self, object):
        try:
            return f'{object.pl_processador.modelo} {object.pl_processador.frequencia}'
        except AttributeError:
            return '-'

class ProcessadorModel(admin.ModelAdmin):
    list_display = ['id', 'marca', 'modelo', 'frequencia', 'memoria_cache']
    list_display_links = ['id', 'marca', 'modelo']


class HdModel(admin.ModelAdmin):
    list_display = ['id', 'modelo', 'tamanho_gb', 'funciona']
    list_display_links = ['id', 'modelo', 'tamanho_gb']
    list_editable = ['funciona']


class GabineteModel(admin.ModelAdmin):
    list_display = ['id', 'modelo', 'tipo', 'usb_frontal']
    list_display_links = ['id', 'modelo', 'tipo']

    def tipo(self, object):
        return object.gabinete_tipo


admin.site.register(Teclado, TecladoModel)
admin.site.register(Mouse, MouseModel)
admin.site.register(Monitor, MonitorModel)
admin.site.register(PlacaMae, PlacaMaeModel)
admin.site.register(Processador, ProcessadorModel)
admin.site.register(Hd, HdModel)
admin.site.register(Gabinete, GabineteModel)