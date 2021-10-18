from django.contrib import admin
from .models import Departamento, Funcionario


class DepartamentoModel(admin.ModelAdmin):
    list_display = ['id', 'departamento','singla_departamento', 'predio']
    list_display_links = ['departamento', 'predio']


class FuncionarioModel(admin.ModelAdmin):
    list_display = ['id', 'nome', 'sobrenome', 'usuario_pc', 'senha_pc' ,'setor', 'acesso']
    list_display_links = ['nome', 'sobrenome']
    fieldsets = (
        ('Informações Pessoais', {'fields': ('nome', 'sobrenome', 'sexo', 'departamento')}),
        ('Acesso Computador', {'fields': ('usuario_pc', 'senha_pc', 'controle_acesso'), }),
        ('Outras Informações', {'fields': ('descricao',),})
    )

    def setor(self, object):
        try: 
            if object.departamento.singla_departamento:
                return object.departamento.singla_departamento
            else:
                return object.departamento.departamento
        except AttributeError:
            return '-'

    def acesso(self, object):
        return object.controle_acesso
        

admin.site.register(Departamento, DepartamentoModel)
admin.site.register(Funcionario, FuncionarioModel)
