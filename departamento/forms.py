from django import forms
from django.forms import widgets
from django.forms.fields import CharField
from django.forms.widgets import Select, SelectMultiple, TextInput, Textarea
from django.db.models import Value as V
from django.db.models.functions import Concat
from .models import Departamento, Funcionario, CHOICES_PREDIOS
from dispositivo.models import CHOICES_SISTEMS

class DepartamentoForm(forms.ModelForm):
    class Meta:
        model = Departamento
        fields = ['predio', 'departamento', 'singla_departamento', 'descricao']

    predio = forms.ChoiceField(label='Prédio', choices=CHOICES_PREDIOS, widget=Select(attrs={'class': 'form-control'}))
    departamento = forms.CharField(max_length=255, widget=TextInput(attrs={'class': 'form-control', 'autocomplete':'off', 'placeholder': 'Exemplo: Informática'}))
    singla_departamento = forms.CharField(label='Sigla Departamento', max_length=5, widget=TextInput(attrs={'class': 'form-control', 'autocomplete':'off', 'placeholder':'Exemplo: TI'}), required=False)
    descricao = forms.CharField(label='Descrição', max_length=1000, widget=Textarea(attrs={'rows':'3','class':'form-control', 'autocomplete':'off', 'placeholder': 'Informações Complementares...'}), required=False)


class FuncionarioForm(forms.ModelForm):
    class Meta:
        model = Funcionario
        fields = [
            'nome', 'sobrenome', 'departamento', 'admin_rede', 'usuario_pc', 'senha_pc',
            'controle_acesso', 'descricao'
        ]

    nome = forms.CharField(label="Nome *" ,widget=TextInput(attrs={'class': 'form-control', 'autocomplete':'off', 'placeholder': 'Exemplo: Fulano'}))
    sobrenome = forms.CharField(label='Sobrenome', required=False, max_length=255, widget=TextInput(attrs={'class': 'form-control', 'autocomplete':'off', 'placeholder': 'Ex: Silva'}))
    departamento = forms.ModelChoiceField(label='Departamento', queryset=(Departamento.objects.all()), widget=Select(attrs={'class': 'form-control'}))
    usuario_pc = forms.CharField(label='Usuário PC' ,widget=TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: fulano.silva'}), required=False)
    senha_pc = forms.CharField(label='Senha PC', max_length=255, widget=TextInput(attrs={'class': 'form-control', 'autocomplete':'off', 'placeholder': 'Ex: Brasil2021'}), required=False)
    
    controle_acesso = forms.ChoiceField(choices=(
        ('Pessimista', 'Pessimista'),
        ('Otimista','Otimista')
        ),widget=Select(attrs={'class': 'form-control'}))

    admin_rede = forms.ChoiceField(choices=(
        ('Não', 'Não'),
        ("Sim",'Sim')
        ),widget=Select(attrs={'class': 'form-control'}))
    
    descricao = forms.CharField(label="Descrição", max_length=1000, widget=Textarea(attrs={'rows':'3','class':'form-control', 'autocomplete':'off', 'placeholder': 'Informações complementares sobre o usuário.'}), required=False)


class FuncionarioVisualizarForm(forms.Form):
    nome_rede = forms.CharField(label='Nome Rede', max_length=20, required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'autocomplete': 'off', 'placeholder':'Exemplo: PRE-01'}))
    usuario_pc = forms.CharField(label='Usuário PC', max_length=100, required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'autocomplete': 'off', 'placeholder':'Ex: gustavo.silva'}))
    senha_pc = forms.CharField(label='Senha PC', max_length=100, required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'autocomplete': 'off', 'placeholder':'Ex: Brasil2021'}))
    sistema_op = forms.ChoiceField(choices=CHOICES_SISTEMS, widget=Select(attrs={'class': 'form-control'}))
    admin_rede = forms.ChoiceField(required=True, choices=(
        ('Não', 'Não'),
        ('Sim', 'Sim')
    ), widget=Select(attrs={'class': 'form-control'}))
    acesso_rede = forms.ChoiceField(choices=(
        ('Pessimista', 'Pessimista'),
        ('Otimista', 'Otimista')
    ), widget=Select(attrs={'class':'form-control'}))