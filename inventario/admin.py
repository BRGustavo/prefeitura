from django.contrib import admin
from django.db.models import fields
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
    list_display = ['id', 'marca', 'hdmi', 'tamanho', 'patrimonio']
    list_display_links = ['id', 'marca']

class PlacaMaeModel(admin.ModelAdmin):
    list_display = ['id', 'marca', 'modelo', 'hdmi', 'suporte','processador']
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
    list_display = ['id', 'modelo', 'tamanho_gb']
    list_display_links = ['id', 'modelo', 'tamanho_gb']


class GabineteModel(admin.ModelAdmin):
    list_display = ['id', 'modelo']
    list_display_links = ['id', 'modelo']

    def tipo(self, object):
        return object.gabinete_tipo


# class MemoriaRamModel(admin.ModelAdmin):
#     list_display = ['id', 'modelo', 'frequencia']
#     list_display_links = ['id', 'modelo', 'frequencia']
#     fieldsets = (
#         ('Acesso Remoto', {'fields': ('modelo', 'frequencia' )}),
#         ('OUTRAS INFORMAÇÕES', {'fields': ('descricao',)})
#     )

admin.site.register(Teclado, TecladoModel)
admin.site.register(Mouse, MouseModel)
admin.site.register(Monitor, MonitorModel)
admin.site.register(PlacaMae, PlacaMaeModel)
admin.site.register(Processador, ProcessadorModel)
admin.site.register(Hd, HdModel)
admin.site.register(Gabinete, GabineteModel)