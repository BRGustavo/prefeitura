from django.db import models
from django.db.models.deletion import CASCADE, PROTECT
from departamento.models import Departamento, Funcionario
from macaddress.fields import MACAddressField
from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django import forms
from inventario.models import *
from django.db.models import Q



CHOICES_BOOL = (
    (True, 'Sim'),
    (False, 'Não')
)

class EnderecoMac(models.Model):
    mac_address = MACAddressField(unique=True, blank=True, null=True)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, blank=True, related_name='mac_parente')
    parent_object_id = models.PositiveIntegerField()
    parent_object = GenericForeignKey("content_type", "parent_object_id")

    def __str__(self) -> str:
        return str(self.mac_address)

class EnderecoIp(models.Model):
    ip_address = models.GenericIPAddressField(verbose_name='Endereço IP',unique=True, blank=True, null=True)
    
    content_type = models.ForeignKey(ContentType, related_name='ip_parente', on_delete=CASCADE)
    parent_object_id = models.PositiveIntegerField()
    parent_object = GenericForeignKey("content_type", "parent_object_id")

    def __str__(self) -> str:
        return str(self.ip_address)

class Roteador(models.Model):

    class Meta:
        verbose_name_plural = 'Roteadores'
        
    ssid = models.CharField(max_length=100, verbose_name="SSID", null=False, help_text="Nome visivel da rede.")
    senha = models.CharField(max_length=100, null=True, blank=True)
    modelo = models.CharField(max_length=50, null=False, choices=[
        ('TP-LINK', 'TP-Link'),
        ('D-Link', 'D-Link'),
        ('Huawei', 'Huawei'),
        ('Outro', 'Outro')
    ])
    multimodo = models.CharField(max_length=1, default='N', choices=[
        ('N', 'Não'),
        ('S', 'Sim')
    ], help_text='Multimodo: Frequência 2.4Ghz e 5Ghz.')
    departamento = models.ForeignKey(Departamento, blank=True, null=True, on_delete=CASCADE)
    descricao = models.TextField(blank=True, verbose_name='Descrição')
    mac_roteador = GenericRelation(EnderecoMac, object_id_field='parent_object_id', related_query_name='roteador')
    ip_roteador = GenericRelation(EnderecoIp, object_id_field='parent_object_id', related_query_name='roteador')

    def __str__(self) -> str:
        return f'Roteador: {self.ssid}'


class Impressora(models.Model):

    TONER_CHOICES = [
        ('Modelo 01', 'Modelo 01'),
        ('Modelo 02', 'Modelo 02'),
        ('Modelo 03', 'Modelo 03')
    ]
    nome = models.CharField(max_length=100, blank=True, null=True, verbose_name='Nome Impressora')
    modelo = models.CharField(max_length=100, null=False, blank=False, verbose_name='Modelo')
    tipo_toner = models.CharField(max_length=100, default=TONER_CHOICES[0], null=False, choices=TONER_CHOICES, verbose_name='Toner')
    local = models.CharField(max_length=10, verbose_name='Local Impressora', default='Sala', choices=(
        ('Sala', 'Sala'),
        ('Corredor', 'Corredor')
    ))
    patrimonio = models.CharField(max_length=50, blank=True, null=True, verbose_name='Patrimônio', help_text='Número do patrimônio')

    sala = models.IntegerField(blank=True, null=True, verbose_name="Número Sala", help_text='Número de refência ao local onde a impressora está.')

    usando_ip = models.BooleanField(verbose_name='Usando IP', help_text='Está conectada pela rede;usando um ip.', default=True, null=False, choices=CHOICES_BOOL)

    pertence_gestpar = models.BooleanField(default=False, null=False, choices=CHOICES_BOOL, verbose_name='Impressora Gestpar', help_text='Impressora alugada')
    gestpar_matricula = models.CharField(max_length=20, blank=True, null=True)
    descricao = models.TextField(verbose_name='Descrição', blank=True, null=True)
    mac_impressora = GenericRelation(EnderecoMac, object_id_field='parent_object_id', related_query_name='impressora')

    ip_impressora = GenericRelation(EnderecoIp, object_id_field='parent_object_id', related_query_name='impressora')

    def __str__(self) -> str:
        # print(f'{EnderecoMac.objects.get(impressora__id=1)}')
        return f'{self.modelo}'

    # def delete(self, *args, **kwargs):
    #     EnderecoMac.objects.filter(content_type='dispositivo | impressora', content_type__id=self.id).delete()
    #     EnderecoIp.objects.filter(content_type='dispositivo | impressora', content_type__id=self.id)
    #     return super(Impressora, self).delete(*args, **kwargs)

class Computador(models.Model):

    class Meta:
        verbose_name = 'Computador'
        verbose_name_plural = 'Computadores'

    CHOICES_SISTEMS = (

        ('Win7', 'Windows 7'),
        ('Win8', 'Windows 8'),
        ('Win10', 'Windows 10'),
        ('Ubuntu', 'Ubuntu'),
        ('WinServer', 'Windows Server')
    )
    departamento = models.ForeignKey(Departamento, blank=True, null=True, on_delete=PROTECT,
    help_text='Departamento ao qual o computador pertence.')
    funcionario = models.ForeignKey(Funcionario, blank=True, null=True, on_delete=PROTECT,
    help_text='Funcionário que utilizará o computador.')
    gabinete = models.OneToOneField(Gabinete, blank=True, null=True, on_delete=PROTECT, )
    placa_mae = models.OneToOneField(PlacaMae, verbose_name='Placa Mãe', blank=True, null=True, on_delete=PROTECT, )
    processador = models.OneToOneField(Processador, blank=True, null=True, on_delete=PROTECT)
    hd = models.OneToOneField(Hd, blank=True, null=True, on_delete=PROTECT, )
    monitor = models.OneToOneField(Monitor, blank=True, null=True, on_delete=PROTECT, )
    teclado = models.OneToOneField(Teclado, blank=True, null=True, on_delete=PROTECT, )
    mouse = models.OneToOneField(Mouse, blank=True, null=True, on_delete=PROTECT, )
    sistema_op = models.CharField(verbose_name='Sistema Operacional', max_length=10, blank=True, choices=CHOICES_SISTEMS)
    sala = models.IntegerField(blank=True, null=True, help_text='Número de referência a sala onde ficará o computador')
    anydesk = models.CharField(max_length=120, verbose_name='AnyDesk', blank=True, null=True)
    mac_computador = GenericRelation(EnderecoMac, object_id_field='parent_object_id', related_query_name='computador')
    ip_computador = GenericRelation(EnderecoIp, object_id_field='parent_object_id', related_query_name='computador')

    def meu_id(self):
        return self.id

    def __str__(self) -> str:
        print()
        modelo, funcionario, departamento = ' '*3
        # try: modelo = f'{self.processador.modelo}'
        # except AttributeError: modelo = ''
        # try: funcionario = f'{self.funcionario.modelo}'
        # except: AttributeError: funcionario = ''
        # try: departamento = f'{self.departamento.departamento}'
        # except AttributeError: departamento = ''

        return f'{modelo} {funcionario} {departamento}'
