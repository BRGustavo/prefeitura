from typing import Text
from django import forms
from django.db.models.base import Model
from django.db.models.query import QuerySet
from django.forms import widgets
from django.forms.fields import IntegerField
from django.forms.models import ModelForm 
from django.forms.widgets import CheckboxSelectMultiple, Input, NumberInput, Select, SelectMultiple, TextInput, Textarea
from macaddress.fields import MACAddressFormField

from inventario.models import Hd, Monitor, Mouse, PlacaMae, Processador, Teclado
from .models import Computador, EnderecoIp, Gabinete, MemoriaRam
from departamento.models import Departamento, Funcionario
from django.db.models import Q 

class ComputadorForm(forms.ModelForm):
    class Meta:
        model = Computador
        fields = [
            'departamento', 'funcionario', 'nome_rede', 'gabinete',
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
        self.fields['hd'].queryset = (
            Hd.objects.all().filter(computador__isnull=True) | (Hd.objects.filter(computador=self.instance))
        )

    CHOICES_SISTEMS = (

        ('Win7', 'Windows 7'),
        ('Win8', 'Windows 8'),
        ('Win10', 'Windows 10'),
        ('Ubuntu', 'Ubuntu'),
        ('WinServer', 'Windows Server')
    )
    sistema_op = forms.ChoiceField(choices=CHOICES_SISTEMS, widget=Select(attrs={'class': 'form-control'}))
    
    departamento = forms.ModelChoiceField(required=False, queryset=(Departamento.objects.all()), widget=Select(attrs={'class': 'form-control'}))
    funcionario = forms.ModelChoiceField(required=False, queryset=(Funcionario.objects.all()), widget=Select(attrs={'class': 'form-control', 'autocomplete':'off'}))
    nome_rede = forms.CharField(widget=TextInput(attrs={'class': 'form-control', 'autocomplete':'off'}))
    anydesk = forms.CharField(required=False, widget=TextInput(attrs={'class': 'form-control', 'autocomplete':'off'}))
    sala = forms.IntegerField(required=False, widget=NumberInput(attrs={'class': 'form-control'}))
    gabinete = forms.ModelChoiceField(queryset=Gabinete.objects.all(), widget=Select(attrs={'class': 'form-control'})) 
    placa_mae = forms.ModelChoiceField(required=False, queryset=PlacaMae.objects.all(), widget=Select(attrs={'class': 'form-control'}))      
    processador = forms.ModelChoiceField(required=False, queryset=Processador.objects.all(), widget=Select(attrs={'class': 'form-control'}))
    hd = forms.ModelChoiceField(required=False, queryset=Hd.objects.all(), widget=Select(attrs={'class': 'form-control'}))
    mouse = forms.ModelChoiceField(required=False, queryset=Mouse.objects.all(), widget=Select(attrs={'class': 'form-control'}))
    teclado = forms.ModelChoiceField(required=False, queryset=Teclado.objects.all(), widget=Select(attrs={'class': 'form-control'}))

    monitor = forms.ModelMultipleChoiceField(required=False, queryset=Monitor.objects.all().filter(computador__isnull=True), widget=forms.SelectMultiple(attrs={'class': 'form-control'}))

    endereco_ip = forms.GenericIPAddressField(required=False, widget=TextInput(attrs={'class': 'form-control', 'autocomplete':'off', 'aria-describedby': 'enderecoiphelp'}))
    endereco_mac = MACAddressFormField(required=False, widget=TextInput(attrs={'class': 'form-control', 'autocomplete':'off'}))

    descricao = forms.CharField(required=False, widget=Textarea(attrs={'rows':'3','class':'form-control', 'autocomplete':'off'}))

class EndereoIpForm(forms.ModelForm):
    class Meta:
        model = EnderecoIp
        fields = ('ip_address',)
        exclude = ()
    
    ip_address = forms.CharField(required=False, widget=TextInput(attrs={'class': 'form-control'}))


class MemoriaRamForm(forms.ModelForm):
    class Meta:
        model = MemoriaRam
        fields = ('modelo', 'frequencia', 'descricao')
