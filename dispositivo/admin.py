from django.contrib import admin
from .models import EnderecoMac, EnderecoIp, Roteador, Impressora
from django.contrib.contenttypes.admin import GenericStackedInline
from django.db.models import Q


class EnderecoMacInline(GenericStackedInline):
    model = EnderecoMac
    min_num = 1
    max_num = 1
    ct_field = "parent_content_type"
    ct_fk_field = "parent_object_id"
    fk_name = "parent_object"


class EnderecoIpInline(GenericStackedInline):
    model = EnderecoIp
    max_num = 1
    ct_field = "parente_conteudo_tipo"
    ct_fk_field = "parente_objeto_id"
    fk_name = "parente_objeto"



class EnderecoMacModel(admin.ModelAdmin):
    list_display = ['mac_address']


class RoteadorModel(admin.ModelAdmin):
    model = Roteador
    inlines = [EnderecoMacInline, EnderecoIpInline]

    list_display = ['id', 'ssid', 'senha', 'modelo', 'multimodo', 'local']
    list_display_links = ['ssid']
    fieldsets = (
        ('Informações do Roteador', {'fields': ('modelo', 'ssid', 'senha')}),
        ('Informações Complementares', {'fields': ('departamento', 'descricao')})
    )
    def local(self, object):
        try:
            return object.departamento.departamento
        except AttributeError:
            return '-'


class ImpressoraModel(admin.ModelAdmin):
    model = Impressora
    inlines = [EnderecoIpInline]

admin.site.register(Roteador, RoteadorModel)
admin.site.register(Impressora, ImpressoraModel)
admin.site.register(EnderecoIp)


