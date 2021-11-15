from typing import Text
from django import forms
from django.db.models.base import Model
from django.db.models.fields import CharField, TextField
from django.db.models.query import QuerySet
from django.forms import widgets
from django.forms.fields import IntegerField
from django.forms.models import ModelForm 
from django.forms.widgets import CheckboxSelectMultiple, Input, NumberInput, Select, SelectMultiple, TextInput, Textarea
from macaddress.fields import MACAddressFormField

from inventario.models import Hd, Monitor, Mouse, PlacaMae, Processador, Teclado
from .models import Computador, EnderecoIp, Gabinete, Impressora, MemoriaRam, Roteador, CHOICES_ROTEADORES, CHOICES_SISTEMS, TONER_CHOICES
from departamento.models import Departamento, Funcionario
from django.db.models import Q 


class ComputadorForm(forms.ModelForm):
    class Meta:
        model = Computador
        fields = [
            'departamento', 'funcionario', 'nome_rede', 'gabinete',
            'placa_mae', 'processador', 'hd', 'monitor', 'teclado', 'mouse', 'sistema_op', 
            'memoria_ram', 'anydesk', 'descricao'
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
        self.fields['monitor'].queryset = (
            Monitor.objects.all().filter(computador__isnull=True) | (Monitor.objects.filter(computador=self.instance))
        )
    sistema_op = forms.ChoiceField(choices=CHOICES_SISTEMS, widget=Select(attrs={'class': 'form-control'}))
    
    departamento = forms.ModelChoiceField(required=False, queryset=(Departamento.objects.all()), widget=Select(attrs={'class': 'form-control'}))
    funcionario = forms.ModelChoiceField(required=False, queryset=(Funcionario.objects.all()), widget=Select(attrs={'class': 'form-control', 'autocomplete':'off'}))
    nome_rede = forms.CharField(widget=TextInput(attrs={'class': 'form-control', 'autocomplete':'off', 'placeholder': 'Exemplo: PRE-01'}))
    anydesk = forms.CharField(required=False, widget=TextInput(attrs={'class': 'form-control', 'autocomplete':'off', 'placeholder': 'Ex: 0000000'}))
    memoria_ram = forms.CharField(required=False, max_length=20, widget=TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: 8 GB'}))
    gabinete = forms.ModelChoiceField(queryset=Gabinete.objects.all(), widget=Select(attrs={'class': 'form-control'})) 
    placa_mae = forms.ModelChoiceField(required=False, queryset=PlacaMae.objects.all(), widget=Select(attrs={'class': 'form-control'}))      
    processador = forms.ModelChoiceField(required=False, queryset=Processador.objects.all(), widget=Select(attrs={'class': 'form-control'}))
    hd = forms.ModelChoiceField(required=False, queryset=Hd.objects.all(), widget=Select(attrs={'class': 'form-control'}))
    mouse = forms.ModelChoiceField(required=False, queryset=Mouse.objects.all(), widget=Select(attrs={'class': 'form-control'}))
    teclado = forms.ModelChoiceField(required=False, queryset=Teclado.objects.all(), widget=Select(attrs={'class': 'form-control'}))

    monitor = forms.ModelMultipleChoiceField(required=False, queryset=Monitor.objects.all().filter(computador__isnull=True), widget=forms.SelectMultiple(attrs={'class': 'form-control'}))

    endereco_ip = forms.GenericIPAddressField(required=False, widget=TextInput(attrs={'class': 'form-control', 'autocomplete':'off', 'aria-describedby': 'enderecoiphelp', 'placeholder': 'Ex: 192.168.5.20'}))
    endereco_mac = MACAddressFormField(required=False, widget=TextInput(attrs={'class': 'form-control', 'autocomplete':'off', 'placeholder': 'Ex: AA-AA-AA-AA-AA-AA'}))

    descricao = forms.CharField(required=False, widget=Textarea(attrs={'rows':'3','class':'form-control', 'autocomplete':'off', 'placeholder': 'Descreve mais sobre o dispositivo.'}))


class RoteadorForm(forms.ModelForm):
    class Meta:
        model = Roteador
        fields = ('ssid', 'senha', 'modelo', 'departamento', 'descricao')
        exclude = ()

    ssid = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Exemplo: Sala do Empreendedor'}))
    senha = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: 12345'}))
    modelo = forms.ChoiceField(required=True, choices=CHOICES_ROTEADORES, widget=forms.Select(attrs={'class': 'form-control'}))
    departamento = forms.ModelChoiceField(required=False, queryset=Departamento.objects.all(), widget=forms.Select(attrs={'class': 'form-control'}))
    descricao = forms.CharField(required=False, widget=Textarea(attrs={'class': 'form-control', 'placeholder': 'Descreva melhor o dispositivo.'}))
    endereco_ip = forms.GenericIPAddressField(required=False, widget=TextInput(attrs={'class': 'form-control', 'autocomplete':'off', 'aria-describedby': 'enderecoiphelp', 'placeholder': 'Exemplo: 192.168.4.20'}))
    endereco_mac = MACAddressFormField(required=False, widget=TextInput(attrs={'class': 'form-control', 'autocomplete':'off', 'placeholder': 'Exemplo: AA-AA-AA-AA-AA-AA'}))


class ImpressoraForm(forms.ModelForm):
    class Meta:
        model = Impressora
        fields = ('nome', 'modelo', 'tipo_toner', 'patrimonio', 'pertence_gestpar', 'gestpar_matricula', 'departamento', 'sala')

    nome = forms.CharField(required=True, widget=TextInput(attrs={'class': 'form-control', 'autocomplete': 'off', 'placeholder': 'Exemplo: Corredor Informática.'}))
    modelo = forms.CharField(required=True, widget=TextInput(attrs={'class': 'form-control', 'autocomplete': 'off', 'placeholder': 'Exemplo: Samsung'}))
    tipo_toner = forms.ChoiceField(required=True, choices=TONER_CHOICES, widget=forms.Select(attrs={'class': 'form-control', 'autocomplete': 'off', 'placeholder': 'Exemplo: Samsung'}))
    patrimonio = forms.CharField(required=False, widget=TextInput(attrs={'class': 'form-control', 'autocomplete': 'off', 'placeholder': 'Ex: 123456'}))
    pertence_gestpar = forms.BooleanField(required=False, widget=Select(attrs={'class':'form-control'}))
    gestpar_matricula = forms.CharField(required=False, widget=TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: GEST-123'}))
    departamento = forms.ModelChoiceField(required=False, queryset=Departamento.objects.all(), widget=forms.Select(attrs={'class': 'form-control'}))
    sala = forms.CharField(required=False, max_length=20, widget=TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: Sala 10'}))
    descricao = forms.CharField(required=False, widget=Textarea(attrs={'class': 'form-control', 'placeholder': 'Descreva melhor o dispositivo.'}))
    endereco_ip = forms.GenericIPAddressField(required=False, widget=TextInput(attrs={'class': 'form-control', 'autocomplete':'off', 'aria-describedby': 'enderecoiphelp', 'placeholder': 'Ex: 192.168.4.20'}))
    endereco_mac = MACAddressFormField(required=False, widget=TextInput(attrs={'class': 'form-control', 'autocomplete':'off', 'placeholder': 'Ex: AA-AA-AA-AA-AA-AA'}))


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
