from django.contrib import admin
from .models import Departamento, Funcionario


class DepartamentoModel(admin.ModelAdmin):
    list_display = ['id', 'departamento','singla_departamento', 'predio']
    list_display_links = ['departamento', 'predio']


class FuncionarioModel(admin.ModelAdmin):
    list_display = ['id', 'nome', 'sobrenome', 'singla', 'acesso']
    list_display_links = ['nome', 'sobrenome']

    def singla(self, object):
        try: 
            return object.departamento.singla_departamento
        except AttributeError:
            return object.departamento.departamento

    def acesso(self, object):
        return object.controle_acesso
        

admin.site.register(Departamento, DepartamentoModel)
admin.site.register(Funcionario, FuncionarioModel)
