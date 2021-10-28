from django import forms
from django.forms import widgets
from django.forms.fields import CharField
from django.forms.widgets import Select, SelectMultiple, TextInput, Textarea
from django.db.models import Value as V
from django.db.models.functions import Concat
import departamento
from .models import Departamento, Funcionario

class DepartamentoForm(forms.ModelForm):
    class Meta:
        model = Departamento
        fields = ['predio', 'departamento', 'singla_departamento', 'descricao']

    CHOICES_PREDIOS = [
        ('Prefeitura Arapoti', 'Prefeitura Municipal de Arapoti'),
        ('Col. Clotário', 'Colégio Clortário Portugal'),
        ('Col. Tel.Carneiro', 'Colégio Telemaco Carneiro'),
        ('Col. D.Zizi', 'Colégio Dona Zizi'),
        ('UBS Jd.Aratinga', 'UBS Jardim Aratinga'),
        ('UBS Jd.Ceres', 'UBS Jardim Ceres'),
        ('UBS Vila Romana', 'UBS Vila Romana'),
        ('CRAS', 'CRAS'),
        ('CREAS', 'CREAS - Centro de Referência Especializado em Assistência Social')
    ]

    predio = forms.ChoiceField(choices=CHOICES_PREDIOS, widget=Select(attrs={'class': 'form-control'}))
    departamento = forms.CharField(max_length=255, widget=TextInput(attrs={'class': 'form-control', 'autocomplete':'off'}))
    singla_departamento = forms.CharField(max_length=5, widget=TextInput(attrs={'class': 'form-control', 'autocomplete':'off'}), required=False)
    descricao = forms.CharField(max_length=1000, widget=Textarea(attrs={'rows':'3','class':'form-control', 'autocomplete':'off'}), required=False)


class FuncionarioForm(forms.ModelForm):
    class Meta:
        model = Funcionario
        fields = [
            'nome', 'sobrenome', 'departamento', 'admin_rede', 'usuario_pc', 'senha_pc',
            'controle_acesso', 'descricao'
        ]

    nome = forms.CharField(widget=TextInput(attrs={'class': 'form-control', 'autocomplete':'off'}))
    sobrenome = forms.CharField(max_length=255, widget=TextInput(attrs={'class': 'form-control', 'autocomplete':'off'}))
    departamento = forms.ModelChoiceField(queryset=(Departamento.objects.all()), widget=Select(attrs={'class': 'form-control'}))
    usuario_pc = forms.CharField(widget=TextInput(attrs={'class': 'form-control'}), required=False)
    senha_pc = forms.CharField(max_length=255, widget=TextInput(attrs={'class': 'form-control', 'autocomplete':'off'}), required=False)
    
    controle_acesso = forms.ChoiceField(choices=(
        ('Pessimista', 'Pessimista'),
        ('Otimista','Otimista')
        ),widget=Select(attrs={'class': 'form-control'}))

    admin_rede = forms.ChoiceField(choices=(
        (False, 'Não'),
        (True,'Sim')
        ),widget=Select(attrs={'class': 'form-control'}))
    
    descricao = forms.CharField(max_length=1000, widget=Textarea(attrs={'rows':'3','class':'form-control', 'autocomplete':'off'}), required=False)