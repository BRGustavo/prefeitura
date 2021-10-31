from django import forms
from django.db.models.query import QuerySet
from django.forms import widgets
from django.forms.fields import IntegerField 
from django.forms.widgets import CheckboxSelectMultiple, Input, NumberInput, Select, SelectMultiple, TextInput

from inventario.models import Hd, Monitor, Mouse, PlacaMae, Processador, Teclado
from .models import Computador, Gabinete
from departamento.models import Departamento, Funcionario
from django.db.models import Q 

class ComputadorForm(forms.ModelForm):
    class Meta:
        model = Computador
        fields = [
            'departamento', 'funcionario', 'nome_rede', 'patrimonio', 'gabinete',
            'placa_mae', 'processador', 'hd', 'monitor', 'teclado', 'mouse', 'sistema_op', 
            'sala', 'anydesk'
        ]

    def __init__(self, *args, **kwargs):
        super(ComputadorForm, self).__init__(*args, **kwargs)
        
        self.fields['gabinete'].queryset = (
            Gabinete.objects.all().filter(computador__isnull=True) | (Gabinete.objects.filter(computador=self.instance))
        )
        self.fields['placa_mae'].queryset = (
            PlacaMae.objects.all().filter(computador__isnull=True) | (PlacaMae.objects.filter(computador=self.instance))
        )
        self.fields['processador'].queryset = (
            Processador.objects.all().filter(computador__isnull=True) | (Processador.objects.filter(computador=self.instance))
        )
        self.fields['teclado'].queryset = (
            Teclado.objects.all().filter(computador__isnull=True) | (Teclado.objects.filter(computador=self.instance))
        )
        self.fields['mouse'].queryset = (
            Mouse.objects.all().filter(computador__isnull=True) | (Mouse.objects.filter(computador=self.instance))
        )


    departamento = forms.ModelChoiceField(required=False, queryset=(Departamento.objects.all()), widget=Select(attrs={'class': 'form-control'}))
    funcionario = forms.ModelChoiceField(required=False, queryset=(Funcionario.objects.all()), widget=Select(attrs={'class': 'form-control'}))
    nome_rede = forms.CharField(widget=TextInput(attrs={'class': 'form-control'}))
    patrimonio = forms.CharField(required=False, widget=TextInput(attrs={'class': 'form-control'}))
    anydesk = forms.CharField(required=False, widget=TextInput(attrs={'class': 'form-control'}))
    sala = forms.IntegerField(required=False, widget=NumberInput(attrs={'class': 'form-control'}))
    gabinete = forms.ModelChoiceField(queryset=Gabinete.objects.all(), widget=Select(attrs={'class': 'form-control'})) 
    placa_mae = forms.ModelChoiceField(required=False, queryset=PlacaMae.objects.all(), widget=Select(attrs={'class': 'form-control'}))      
    processador = forms.ModelChoiceField(required=False, queryset=Processador.objects.all(), widget=Select(attrs={'class': 'form-control'}))
    hd = forms.ModelChoiceField(required=False, queryset=Hd.objects.all(), widget=Select(attrs={'class': 'form-control'}))
    mouse = forms.ModelChoiceField(required=False, queryset=Mouse.objects.all(), widget=Select(attrs={'class': 'form-control'}))
    teclado = forms.ModelChoiceField(required=False, queryset=Teclado.objects.all(), widget=Select(attrs={'class': 'form-control'}))

    monitor = forms.ModelMultipleChoiceField(queryset=Monitor.objects.all().filter(computador__isnull=True), widget=forms.SelectMultiple())