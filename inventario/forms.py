from django import forms
from django.forms import widgets
from django.forms.fields import CharField
from django.forms.widgets import Select, SelectMultiple, TextInput, Textarea
from django.db.models import Value as V
from django.db.models.functions import Concat
from .models import CHOICES_MODELS, Gabinete, Monitor, Mouse, PlacaMae, Processador, Teclado, Hd
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
        fields = ('id', )

class ProcessadorForm(forms.ModelForm):
    class Meta:
        model = Processador
        fields = ('id', )

class MonitorForm(forms.ModelForm):
    class Meta:
        model = Monitor
        fields = ('id', )

class HdForm(forms.ModelForm):
    class Meta:
        model = Hd
        fields = ('id', )