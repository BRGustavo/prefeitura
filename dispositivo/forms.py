from typing import Text
from django import forms
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError
from django.core.validators import validate_ipv4_address
from django.db.models.base import Model
from django.db.models.fields import CharField, TextField
from django.db.models.query import QuerySet
from django.db.utils import IntegrityError
from django.forms import widgets
from django.forms.fields import IntegerField
from django.forms.models import ModelForm 
from django.forms.widgets import CheckboxSelectMultiple, Input, NumberInput, PasswordInput, Select, SelectMultiple, TextInput, Textarea
from django.shortcuts import get_object_or_404
from macaddress.fields import MACAddressFormField
from netaddr.eui import EUI

from inventario.models import Hd, Monitor, Mouse, PlacaMae, Processador, Teclado
from .models import Computador, EnderecoIp, EnderecoMac, Gabinete, Impressora, MemoriaRam, Roteador, CHOICES_ROTEADORES, CHOICES_SISTEMS
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

    descricao = forms.CharField(required=False, widget=Textarea(attrs={'rows':'8','class':'form-control', 'autocomplete':'off', 'placeholder': 'Descreve mais sobre o dispositivo.'}))


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
        fields = ('nome', 'modelo', 'patrimonio', 'pertence_gestpar', 'gestpar_matricula', 'departamento', 'sala')

    nome = forms.CharField(required=True, widget=TextInput(attrs={'class': 'form-control', 'autocomplete': 'off', 'placeholder': 'Exemplo: Corredor Informática.'}))
    modelo = forms.CharField(required=True, widget=TextInput(attrs={'class': 'form-control', 'autocomplete': 'off', 'placeholder': 'Exemplo: Samsung'}))
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


class ComputadorFormDescricao(forms.ModelForm):
    class Meta:
        model = Computador
        fields = ('descricao',)
    
    descricao = forms.CharField(required=False, widget=Textarea(attrs={'rows':'8','class':'form-control', 'autocomplete':'off', 'placeholder': 'Descreve mais sobre o dispositivo.'}))

class ComputadorFormInfo(forms.ModelForm):
    class Meta:
        model = Computador
        fields = ('nome_rede', 'sistema_op', 'memoria_ram', 'anydesk', 'placa_mae')

    def __init__(self, *args, **kwargs):
        super(ComputadorFormInfo, self).__init__(*args, **kwargs)
        
        self.fields['placa_mae'].queryset = (
            PlacaMae.objects.all().filter(computador__isnull=True) | (PlacaMae.objects.filter(computador=self.instance))
        )
        self.fields['hd'].queryset = (
            Hd.objects.all().filter(computador__isnull=True) | (Hd.objects.filter(computador=self.instance))
        )
        if Monitor.objects.filter(computador=self.instance).count() >=1:
            self.fields['monitor1'].initial = Monitor.objects.filter(computador=self.instance).first().patrimonio

        if Monitor.objects.filter(computador=self.instance).count() >=2:
            self.fields['monitor2'].initial = Monitor.objects.filter(computador=self.instance)[1].patrimonio

    sistema_op = forms.ChoiceField(choices=CHOICES_SISTEMS, widget=Select(attrs={'class': 'form-control'}))
    nome_rede = forms.CharField(widget=TextInput(attrs={'class': 'form-control', 'autocomplete':'off', 'placeholder': 'Exemplo: PRE-01'}))
    anydesk = forms.CharField(required=False, widget=TextInput(attrs={'class': 'form-control', 'autocomplete':'off', 'placeholder': 'Ex: 0000000'}))
    memoria_ram = forms.CharField(required=False, max_length=20, widget=TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: 8 GB'}))
    gabinete = forms.CharField(required=False, widget=TextInput(attrs={'class': 'form-control', 'placeholder': 'Patrimônio Gabinete'})) 
    placa_mae = forms.ModelChoiceField(required=False, queryset=PlacaMae.objects.all(), widget=Select(attrs={'class': 'form-control'}))
    hd = forms.CharField(required=False, widget=TextInput(attrs={'class': 'form-control', 'autocomplete': 'false'}))

    monitor1 = forms.CharField(required=False, widget=TextInput(attrs={'class': 'form-control', 'autocomplete': 'false', 'placeholder': 'Número Patrimônio'}))
    monitor2 = forms.CharField(required=False, widget=TextInput(attrs={'class': 'form-control', 'autocomplete': 'false', 'placeholder': 'Número Patrimônio'}))

class IpMacFormAtualizar(forms.Form):
    object_id = forms.IntegerField(label='Modal ID Objeto', required=False, widget=TextInput(attrs={'class': 'form-control', '':''}))
    parent_object_id = forms.IntegerField(label='Modal ID Objeto', required=False, widget=TextInput(attrs={'class': 'form-control', '':''}))
    ip_address = forms.CharField(label='Endereço IP', required=False, widget=TextInput(attrs={'class': 'form-control', 'placeholder': 'Exemplo: 192.168.5.1'}))
    endereco_mac = MACAddressFormField(label='Endereço MAC', required=False, widget=TextInput(attrs={'class': 'form-control', 'autocomplete':'off', 'placeholder': 'Exemplo: AA-AA-AA-AA-AA-AA'}))


class ComputadorFormNovo(forms.Form):
    usuario = forms.CharField(label='Usuário', required=False, max_length=30, widget=TextInput(attrs={
        'placeholder': 'Exemplo: gustavo.silva',
        'class': 'form-control bg-success border-0 inputplaceholder',
        'type': 'hidden',
        'autocomplete': 'off',
    }))
    senha = forms.CharField(label='Senha', required=False, max_length=50, widget=PasswordInput(attrs={
        'placeholder': 'Senha Acesso',
        'class': 'form-control bg-success border-0 inputplaceholder',
        'type': 'hidden',
        'autocomplete': 'off',
    }))
    departamento = forms.ModelChoiceField(queryset=Departamento.objects.all(), required=False, widget=Select(attrs={
        'class': 'form-control inputplaceholder bg-success',
        'style': 'font-family: "Arial, Helvetica, sans-serif";',
        'type': 'hidden'
    }))
    nome_rede = forms.CharField(max_length=20, widget=TextInput(attrs={
        'placeholder': 'Exemplo: PRE-10',
        'class': 'form-control',
        'autocomplete': 'off',
    }))
    sistema_op = forms.ChoiceField(label='Sistema Operacional', choices=CHOICES_SISTEMS, widget=forms.Select(attrs={
        'class': 'form-control'
    }))
    anydesk = forms.CharField(max_length=15,required=False, widget=TextInput(attrs={
        'placeholder': 'Exemplo: 153 154 211',
        'class': 'form-control',
        'autocomplete': 'off',
    }))
    processador = forms.CharField(label='Processador', required=False, max_length=15, widget=TextInput(attrs={
        'placeholder': 'Exemplo: Core i9 10ª',
        'class': 'form-control',
        'autocomplete': 'off',
    }))
    memoria_ram = forms.CharField(label='Memória RAM', required=False, max_length=10, widget=TextInput(attrs={
        'placeholder': 'Ex: 8 GB',
        'class': 'form-control',
        'autocomplete': 'off',
    }))
    hd = forms.CharField(label='HD', max_length=10, required=False, widget=TextInput(attrs={
        'placeholder': 'Ex: 500 GB',
        'class': 'form-control',
        'autocomplete': 'off',
    }))
    ip_endereco = forms.GenericIPAddressField(label="Endereço IP", required=False, widget=TextInput(attrs={
        'placeholder': 'Ex: 192.168.0.10',
        'class': 'form-control',
        'autocomplete': 'off',
    }))
    endereco_mac = MACAddressFormField(required=False, widget=TextInput(attrs={
        'class': 'form-control', 
        'autocomplete':'off', 
        'placeholder': 'Ex: AA-AA-AA-AA-AA-AA',
        'autocomplete': 'off',
    }))
    gabinete_patrimonio = forms.CharField(label='Patrimônio Gabinete', required=False, max_length=20, widget=TextInput(attrs={
        'placeholder': 'Ex: 002343',
        'class': 'form-control',
        'autocomplete': 'off',
    }))
    monitor_patrimonio = forms.CharField(label='Patrimônio Monitor', required=False, max_length=20, widget=TextInput(attrs={
        'placeholder': 'Ex: 002343',
        'class': 'form-control',
        'autocomplete': 'off',
    }))

    def clean(self):
        
        cleaned_data = self.cleaned_data

        ip_formulario = cleaned_data.get('ip_endereco')
        departamento_formulario = cleaned_data.get('departamento')
        mac_formulario = cleaned_data.get('endereco_mac')
        if ip_formulario is not None and len(ip_formulario) >=1:
            try: 
                if validate_ipv4_address(ip_formulario) is None:
                    if EnderecoIp.objects.filter(ip_address=ip_formulario).count() >=1:
                        raise forms.ValidationError({'ip_endereco': 'Esse endereço de IP já está sendo utilizado.'})
            except ValidationError as e:
                raise forms.ValidationError(e)
        
        if departamento_formulario is not None:
            if departamento_formulario:
                print("Sim")
            else:
                raise forms.ValidationError({'departamento': 'Esse departamento informado não existe.'})

        if mac_formulario is not None:
            if isinstance(mac_formulario, EUI):
                pass
            else:
                raise forms.ValidationError({'endereco_mac': 'Endereço MAC informado é inválido.'})
                
        return cleaned_data

    def save(self):
        data = self.cleaned_data
        computador = None
        componentes = {
            'gabinete': None,
            'hd': None,
            'ip': None,
            'processador': None,
            'mac': None,
            'usuario': None
        }
        componentes['computador'] = Computador(nome_rede=data['nome_rede'], anydesk=data['anydesk'], sistema_op=data['sistema_op'], memoria_ram=data['memoria_ram'])
        componentes['computador'].save()

        computador = Computador.objects.filter(id=componentes['computador'].id)

        if data['gabinete_patrimonio'] is not None and len(data['gabinete_patrimonio']) >=1:
            componentes['gabinete'] = Gabinete(patrimonio=data['gabinete_patrimonio'], modelo='Outro', descricao='Genérico')
        else:
            componentes['gabinete'] = Gabinete(modelo='Outro', descricao='Genérico')
        
        componentes['gabinete'].save()
        computador.update(gabinete=componentes['gabinete'])

        if data['ip_endereco'] is not None and len(data['ip_endereco']) >=1:
            componentes['ip'] = EnderecoIp(ip_address=data['ip_endereco'], content_type=ContentType.objects.get(model='computador'), parent_object_id=computador.first().id)
            componentes['ip'].save()
            computador.first().ip_computador.add(componentes['ip'])
    
        if data['endereco_mac'] is not None:
            try:
                componentes['mac'] = EnderecoMac(mac_address=data['endereco_mac'], content_type=ContentType.objects.get(model='computador'), parent_object_id=computador.first().id)
                componentes['mac'].save()
                computador.first().mac_computador.add(componentes['mac'])
            except IntegrityError:
                return self.abortar(computador.first().id)

        if data['processador'] is not None and len(data['processador']) >=1:
            componentes['processador'] = Processador(marca='Intel', modelo=data['processador'], descricao='Genérico')
            componentes['processador'].save()
            computador.update(processador=componentes['processador'])

        if data['hd'] is not None and len(data['hd']) >=1:
            componentes['hd'] = Hd(modelo='Normal', tamanho_gb=0, descricao="Genérico")
            componentes['hd'].tamanho = data['hd']
            componentes['hd'].save()
            computador.update(hd=componentes['hd'])

        if data['usuario'] is not None and len(data['usuario']) >=1:
            if data['senha'] is None or len(data['senha']) <=1:
                data['senha'] = ''

            usuario = data['usuario']
            consulta_usuario = Funcionario.objects.filter(usuario_pc=usuario)
            if consulta_usuario and consulta_usuario.count() >=1:
                componentes['usuario'] = consulta_usuario.first()
            else:
                if '.' in usuario:
                    local = usuario.find('.')
                    nome_usuario = usuario[:local]
                    sobrenome_usuario = usuario[local+1:]
                    componentes['usuario'] = Funcionario(nome=nome_usuario, sobrenome=sobrenome_usuario, nome_usuario=usuario.lower(), senha_pc=data['senha'])
                    componentes['usuario'].save()

                else:
                    nome_usuario = usuario

                    componentes['usuario'] = Funcionario(nome=nome_usuario, usuario_pc=nome_usuario, senha_pc=data['senha'])
                    componentes['usuario'].save()
                
                if data['departamento'] is not None:
                    Funcionario.objects.filter(id=componentes['usuario'].id).update(departamento=data['departamento'])

            computador.update(funcionario=componentes['usuario'])  

    def abortar(self, id):
        computador = Computador.objects.get(id=id)
        computador.delete()
        Processador.objects.filter(computador=computador).delete()
        Gabinete.objects.filter(computador=computador).delete()
        EnderecoMac.objects.filter(content_type=ContentType.objects.get(model='computador'), parent_object_id=computador.id).delete()
        EnderecoIp.objects.filter(content_type=ContentType.objects.get(model='computador'), parent_object_id=computador.id).delete()
        Hd.objects.filter(computador=computador).delete()

        raise ValueError('Ocorreu um erro ao salvar o computador. Por favor, tente novamente.')