from django import forms
from django.forms import widgets
from django.forms.fields import CharField
from django.forms.widgets import Select, SelectMultiple, TextInput, Textarea
from django.db.models import Value as V
from django.db.models.functions import Concat
from .models import CHOICES_SIM_NAO, CHOICES_TIPO_HD, CHOICES_MODELS, Gabinete, Monitor, Mouse, PlacaMae, Processador, Teclado, Hd
from inventario import models

class TecladoForm(forms.ModelForm):
    class Meta:
        model = Teclado
        fields = ['marca', 'usb', 'descricao']

    marca = forms.CharField(required=False, label='Marca Teclado', widget=TextInput(attrs={'class': 'form-control',
    'autocomplete': 'off'}))
    usb = forms.ChoiceField(label='Entrada USB?', choices=(('True', 'Sim'), ('False', 'Não')),
    widget=Select(attrs={"class": 'form-control'}))
    descricao = forms.CharField(label='Descrição', required=False, widget=Textarea(attrs={'class': 'form-control', 'placeholder': 'Descreva melhor o dispositivo.', 'rows': '2'}))


class MouseForm(forms.ModelForm):
    class Meta:
        model = Mouse
        fields = ['marca', 'usb', 'descricao']

    marca = forms.CharField(required=False, label='Marca Mouse', widget=TextInput(attrs={'class': 'form-control',
    'autocomplete': 'off'}))
    usb = forms.ChoiceField(label='Entrada USB?', choices=(('True', 'Sim'), ('False', 'Não')),
    widget=Select(attrs={"class": 'form-control'}))
    descricao = forms.CharField(label='Descrição', required=False, widget=Textarea(attrs={'class': 'form-control', 'placeholder': 'Descreva melhor o dispositivo.', 'rows': '2'}))

class GabineteForm(forms.ModelForm):
    class Meta:
        model = Gabinete
        fields = ['patrimonio', 'modelo', 'descricao']
    
    patrimonio = forms.CharField(label='Patrimônio Número', required=False, widget=TextInput(attrs={'class': 'form-control', 'autocomplete': 'off'}))
    modelo = forms.ChoiceField(label='Modelo Gabinete', required=False, choices=CHOICES_MODELS, widget=Select(attrs={
        "class": 'form-control', "autocomplete": 'off'
    }))
    descricao = forms.CharField(label='Descrição', required=False, widget=Textarea(attrs={'class': 'form-control', 'placeholder': 'Descreva melhor o dispositivo.', 'rows': '2'}))

class PlacaMaeForm(forms.ModelForm):
    class Meta:
        model = PlacaMae
        fields = ('marca', 'modelo', 'hdmi', 'processador_suporte', 'ram_suporte', 'socket', 'descricao')

    marca = forms.CharField(label='Marca Placa Mãe', required=True, max_length=50, widget=TextInput(attrs={'class': 'form-control', 'autocomplete':'off', 'placeholder': 'Ex: Gigabyte'}))
    modelo = forms.CharField(label='Modelo Placa', max_length=50, required=True, widget=TextInput(attrs={'class':'form-control', 'autocomplete':'off', 'placeholder': 'Ex: Z490M'}))
    hdmi = forms.ChoiceField(required=True, label='Entrada HDMI', choices=CHOICES_SIM_NAO, widget=Select(attrs={'class': 'form-control'}))

    processador_suporte = forms.ChoiceField(label='Processador Suporte', widget=Select(attrs={'class':'form-control'}), choices=[
        ('Intel', 'Intel'),
        ('AMD', 'AMD')
    ])
    ram_suporte = forms.ChoiceField(label='Memória RAM', widget=Select(attrs={'class':'form-control'}), choices=[
        ('DDR1', 'DDR1'),
        ('DDR2', 'DDR2'),
        ('DDR3', 'DDR3'),
        ('DDR4', 'DDR4'),
        
    ])

    socket = forms.CharField(required=False, label='Socket Processador', widget=TextInput(attrs={'class': 'form-control', 'autocomplete':'off', 'placeholder': 'Socket 1155'}))
    descricao = forms.CharField(label='Descrição', required=False, widget=Textarea(attrs={'class': 'form-control', 'placeholder': 'Descreva melhor o dispositivo.', 'rows': '2'}))


class ProcessadorForm(forms.ModelForm):
    class Meta:
        model = Processador
        fields = ('marca', 'modelo', 'frequencia', 'memoria_cache', 'descricao')

    marca = forms.ChoiceField(label='Fabricante', required=True, widget=Select(attrs={'class': 'form-control'}), choices=[('Intel', 'Intel'), ('AMD', 'AMD')])
    modelo = forms.CharField(label='Modelo *', max_length=50, required=True, widget=TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: i5-4ª'}))

    frequencia = forms.FloatField(required=False,label='Frequência', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: 2.33'}))
    memoria_cache = forms.IntegerField(required=False, label='Memória Cache', widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Ex: 4'}))
    descricao = forms.CharField(label='Descrição', required=False, widget=Textarea(attrs={'class': 'form-control', 'placeholder': 'Descreva melhor o dispositivo.', 'rows': '2'}))


class MonitorForm(forms.ModelForm):
    class Meta:
        model = Monitor
        fields = ('marca', 'hdmi', 'tamanho', 'patrimonio', 'descricao')
    
    marca = forms.CharField(required=True, label='Marca Monitor', widget=TextInput(attrs={'class':'form-control', 'placeholder': 'Ex: LG', 'autocomplete': 'off'}))
    hdmi = forms.ChoiceField(required=True, label='HDMI', choices=CHOICES_SIM_NAO, widget=Select(attrs={'class': 'form-control'}))

    tamanho = forms.CharField(required=False, max_length=155, label='Tamanho Tela', widget=TextInput(attrs={'class':'form-control', 'placeholder': 'Ex: 200x300', 'autocomplete': 'off'}))
    patrimonio = forms.CharField(max_length=50, required=False, label='Patrimônio', widget=TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: 1234', 'autocomplete': 'off'}))
    descricao = forms.CharField(label='Descrição', required=False, widget=Textarea(attrs={'class': 'form-control', 'placeholder': 'Descreva melhor o dispositivo.', 'rows': '2'}))


class HdForm(forms.ModelForm):
    class Meta:
        model = Hd
        fields = ('modelo', 'tamanho_gb', 'descricao')

    modelo = forms.ChoiceField(label='Tipo HD', choices=CHOICES_TIPO_HD, widget=Select(attrs={'class': 'form-control'}))

    tamanho_gb = forms.IntegerField(label='Tamanho (GB)', required=True, widget=forms.NumberInput(attrs={'class': 'form-control'}))

    descricao = forms.CharField(label='Descrição', required=False, widget=Textarea(attrs={'class': 'form-control', 'placeholder': 'Descreva melhor o dispositivo.', 'rows': '2'}))
