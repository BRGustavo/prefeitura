from django.db import models
from django.db.models.deletion import CASCADE, PROTECT, SET_NULL
from django.db.models.fields import CharField
from macaddress.fields import MACAddressField
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType

CHOICES_BOLEAN = [
    (True, 'Sim'),
    (False, "Não")
]

class Teclado(models.Model):
    marca = models.CharField(max_length=50, null=False)
    usb = models.BooleanField(null=False, default=True, choices=CHOICES_BOLEAN)
    funciona = models.BooleanField(null=False, default=True, choices=CHOICES_BOLEAN)
    descricao = models.TextField(blank=True)

    def __str__(self) -> str:
        return f'{self.marca}'

class Mouse(models.Model):
    marca = models.CharField(max_length=50, null=False)
    usb = models.BooleanField(null=False, default=True, choices=CHOICES_BOLEAN)
    funciona = models.BooleanField(null=False, default=True, choices=CHOICES_BOLEAN)
    descricao = models.TextField(blank=True)

    def __str__(self) -> str:
        return f'{self.marca}'


class Monitor(models.Model):
    
    class Meta:
        verbose_name_plural = 'Monitores'

    marca = models.CharField(max_length=50, null=False)
    hdmi = models.BooleanField(null=False, default=False, choices=CHOICES_BOLEAN)
    tamanho = models.CharField(max_length=15, blank=True)
    patrimonio = models.CharField(max_length=50, blank=True, null=True, verbose_name='Patrimônio', help_text='Número do patrimônio')
    descricao = models.TextField(blank=True)

    def __str__(self) -> str:
        return f'{self.marca} {self.hdmi}'


class PlacaMae(models.Model):
    
    class Meta:
        verbose_name = 'Placas Mãe'
        verbose_name_plural = 'Placas Mãe'

    marca = models.CharField(max_length=50, null=False)
    modelo = models.CharField(max_length=50)
    hdmi = models.BooleanField(null=False, default=False, choices=CHOICES_BOLEAN)
    processador_suporte = models.CharField(max_length=10, null=False, choices=[
        ('Intel', 'Intel'),
        ('AMD', 'AMD')
    ])
    socket = models.CharField(max_length=50, blank=True)
    funciona = models.BooleanField(null=False, default=True, choices=CHOICES_BOLEAN)
    descricao = models.TextField(blank=True)
    pl_processador = models.OneToOneField('Processador', blank=True, null=True, on_delete=CASCADE)

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
    frequencia = models.FloatField(blank=True)
    memoria_cache = models.IntegerField(blank=True, default=0)
    descricao = models.TextField(verbose_name='Descrição', blank=True)

    def __str__(self) -> str:
        return f'{self.marca}- {self.modelo} - {self.frequencia}'


class Hd(models.Model):
    modelo = models.CharField(max_length=50, null=False, default='Normal', choices=[
        ('Normal', 'Normal'),
        ('Notebook', 'Notebook'),
        ('HD Externo', 'HD Externo')
    ])
    tamanho_gb = models.IntegerField(verbose_name='Tamanho GB', null=False)
    descricao = models.TextField(blank=True)

    def __str__(self) -> str:
        return f'Modelo: {self.modelo} GB: {self.tamanho_gb} Modelo: {self.modelo}'

class Gabinete(models.Model):
    CHOICES_MODELS = [
        ('Positivo', 'Positivo'),
        ('Daten', 'Daten'),
        ('Outro', 'Outro')
    ]
    GABINETE_TIPO = [
        ('Normal', 'Normal'),
        ('Gabinete Horizontal', 'Gabinete Horizontal')
    ]
    modelo = models.CharField(max_length=50, null=False, choices=CHOICES_MODELS)
    gabinete_tipo = models.CharField(max_length=100, default='Normal', null=False, choices=GABINETE_TIPO)
    usb_frontal = models.BooleanField(default=True, choices=[(True, 'Sim'), (False, 'Não')])
    descricao = models.TextField(blank=True)

    def __str__(self) -> str:
        return f'Modelo: {self.modelo} Tipo: {self.gabinete_tipo} usb frontal: {self.usb_frontal}'


class MemoriaRam(models.Model):
    class Meta:
        verbose_name = 'Memória RAM'
        verbose_name_plural = 'Memórias RAM'
    
    modelo = models.CharField(max_length=5, default='DDR4', blank=False, choices=(
        ('DDR', 'DDR'),
        ('DDR2', 'DDR2'),
        ('DDR3', 'DDR3'),
        ('DDR4', 'DDR4'),
        ('DDR5', 'DDR5'),
    ))
    frequencia = models.FloatField(blank=True, null=True, verbose_name='Frequência')
    descricao = models.TextField(blank=True, null=True, verbose_name='Descrição')
