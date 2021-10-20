from django.contrib import admin
from django.forms import forms
from .models import EnderecoMac, EnderecoIp, Roteador, Impressora, Computador
from django.contrib.contenttypes.admin import GenericStackedInline
from django.db.models import Q
from django import forms


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


class ImpressoraAdminForm(forms.ModelForm):
    class Meta:
        model = Impressora
        fields = '__all__'

    def clean(self):
        data = self.cleaned_data
        try:
            if data['pertence_gestpar']:
                if len(data['gestpar_matricula']) <=0:
                    raise forms.ValidationError('A matricula da Gestpar não foi adicionada')
        except TypeError:
            raise forms.ValidationError('A matricula da Gestpar não foi adicionada')
        return self.cleaned_data


class ImpressoraModel(admin.ModelAdmin):
    model = Impressora
    form = ImpressoraAdminForm
    inlines = [EnderecoMacInline, EnderecoIpInline]

    fieldsets = (
        ('INFORMAÇÕES IMPRESSORA', {'fields': ('modelo', 'tipo_toner', 'usando_ip')}),
        ('GESTPAR INFORMAÇÕES', {'fields': ('pertence_gestpar', 'gestpar_matricula')}),
        ('LOCAL INFORMAÇÕES', {'fields': ('sala', 'descricao')})
    )

    list_display = ['modelo', 'tipo_toner', 'usando_ip', 'gestpar', 'sala']

    def gestpar(self, object):
        return object.pertence_gestpar


class ComputadorModel(admin.ModelAdmin):
    inlines = [EnderecoMacInline, EnderecoIpInline]
    list_display = ['funcionario', 'departamento', 'processador', 'sistema_op']
    fieldsets = (
        ('DEPARTAMENTO E FUNCIONARIO', {'fields': ('funcionario', 'departamento', 'sala')}),
        ('COMPONENTES COMPUTADOR', {'fields': ('sistema_op', 'monitor', 'teclado', 'mouse', 'gabinete', 'placa_mae', 'processador', 'hd')})
    )
    def has_delete_permission(self, request, obj=None):
        return False
    

admin.site.register(Roteador, RoteadorModel)
admin.site.register(Impressora, ImpressoraModel)
admin.site.register(Computador, ComputadorModel)

