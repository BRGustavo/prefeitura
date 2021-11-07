from django.db import models
from django.db.models.deletion import CASCADE, PROTECT, SET_NULL
from django.db.models.fields import CharField, reverse_related
from macaddress.fields import MACAddressField
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType

CHOICES_BOLEAN = [
    (True, 'Sim'),
    (False, "Não")
]
CHOICES_SIM_NAO = [
    ('Sim', 'Sim'),
    ('Não', 'Não')
]
CHOICES_MODELS = [
    ('Positivo', 'Positivo'),
    ('Daten', 'Daten'),
    ('Outro', 'Outro')
]
CHOICES_TIPO_HD = [
    ('Normal', 'Normal'),
    ('Notebook', 'Notebook'),
    ('HD Externo', 'HD Externo')
]
class Teclado(models.Model):
    marca = models.CharField(max_length=50, null=False)
    usb = models.BooleanField(null=False, default=True, choices=CHOICES_BOLEAN)
    funciona = models.BooleanField(null=False, default=True, choices=CHOICES_BOLEAN)
    descricao = models.TextField(blank=True)
    criado_data = models.DateTimeField(null=True, blank=True, auto_now_add=True)

    def __str__(self) -> str:
        return f'{self.marca}'

class Mouse(models.Model):
    marca = models.CharField(max_length=50, null=False)
    usb = models.BooleanField(null=False, default=True, choices=CHOICES_BOLEAN)
    funciona = models.BooleanField(null=False, default=True, choices=CHOICES_BOLEAN)
    descricao = models.TextField(blank=True)
    criado_data = models.DateTimeField(null=True, blank=True, auto_now_add=True)

    def __str__(self) -> str:
        return f'{self.marca}'


class Monitor(models.Model):
    
    class Meta:
        verbose_name_plural = 'Monitores'

    marca = models.CharField(max_length=50, null=False)
    hdmi = models.CharField(max_length=10, null=False, blank=True, default='Não', choices=CHOICES_SIM_NAO)
    tamanho = models.CharField(max_length=15, blank=True, null=True)
    patrimonio = models.CharField(max_length=50, blank=True, null=True, verbose_name='Patrimônio', help_text='Número do patrimônio')
    descricao = models.TextField(blank=True, null=True)
    criado_data = models.DateTimeField(null=True, blank=True, auto_now_add=True)

    def __str__(self) -> str:
        return f'Patrimônio: {self.patrimonio} ({self.marca} {self.tamanho})'


class PlacaMae(models.Model):
    class Meta:
        verbose_name = 'Placas Mãe'
        verbose_name_plural = 'Placas Mãe'

    marca = models.CharField(max_length=50, null=False)
    modelo = models.CharField(max_length=50)
    hdmi = models.CharField(max_length=10, null=False, default='Não', choices=CHOICES_SIM_NAO)
    processador_suporte = models.CharField(max_length=10, null=False, choices=[
        ('Intel', 'Intel'),
        ('AMD', 'AMD')
    ])
    socket = models.CharField(max_length=50, blank=True)
    descricao = models.TextField(blank=True)
    criado_data = models.DateTimeField(null=True, blank=True, auto_now_add=True)

    def __str__(self) -> str:
        return f'Marca: {self.marca} Modelo: {self.modelo} Processador: {self.processador_suporte}'


class Processador(models.Model):
    
    class Meta:
        verbose_name_plural = 'Processadores'

    marca = models.CharField(verbose_name='modelo', max_length=20, null=False, choices=[
        ('Intel', 'Intel'),
        ('AMD', 'AMD')
    ])
    modelo = models.CharField(max_length=50, blank=True)
    frequencia = models.FloatField(blank=True, null=True)
    memoria_cache = models.IntegerField(blank=True, null=True, default=0)
    descricao = models.TextField(verbose_name='Descrição', blank=True)
    criado_data = models.DateTimeField(null=True, blank=True, auto_now_add=True)

    def __str__(self) -> str:
        return f'{self.marca}- {self.modelo} - {self.frequencia}'


class Hd(models.Model):
    modelo = models.CharField(max_length=50, null=False, default='Normal', choices=CHOICES_TIPO_HD)
    tamanho_gb = models.IntegerField(verbose_name='Tamanho GB', null=False)
    descricao = models.TextField(blank=True)
    criado_data = models.DateTimeField(null=True, blank=True, auto_now_add=True)

    def __str__(self) -> str:
        return f'Modelo: {self.modelo} GB: {self.tamanho_gb} Modelo: {self.modelo}'

class Gabinete(models.Model):

    patrimonio = models.CharField(max_length=50, blank=True, null=True, verbose_name='Patrimônio', help_text='Número do patrimônio')
    modelo = models.CharField(max_length=50, null=False, choices=CHOICES_MODELS)
    descricao = models.TextField(blank=True)

    criado_data = models.DateTimeField(null=True, blank=True, auto_now_add=True)

    def __str__(self) -> str:
        return f'Patrimônio: {self.patrimonio} ({self.modelo})'


