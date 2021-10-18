from django.db import models
from django.db.models.deletion import CASCADE, PROTECT
from departamento.models import Departamento
from macaddress.fields import MACAddressField
from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType


CHOICES_BOOL = (
    (True, 'Sim'),
    (False, 'Não')
)

class EnderecoMac(models.Model):
    mac_address = MACAddressField(unique=True, blank=True, null=True)
    parent_content_type = models.ForeignKey(ContentType, blank=True, related_name='mac_parente', on_delete=CASCADE)
    parent_object_id = models.PositiveIntegerField()
    parent_object = GenericForeignKey("parent_content_type", "parent_object_id")

    def __str__(self) -> str:
        return str(self.mac_address)

class EnderecoIp(models.Model):
    ip_address = models.GenericIPAddressField(verbose_name='Endereço IP',unique=True, blank=True, null=True)
    
    parente_conteudo_tipo = models.ForeignKey(ContentType, related_name='ip_parente', on_delete=CASCADE)
    parente_objeto_id = models.PositiveIntegerField()
    parente_objeto = GenericForeignKey("parente_conteudo_tipo", "parente_objeto_id")

    def __str__(self) -> str:
        return str(self.ip_address)

class Roteador(models.Model):

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
    endereco_mac = GenericRelation(EnderecoMac, content_type_field='mac_parente')
    endereco_ip = GenericRelation(EnderecoIp, related_query_name='Roteador')

    def __str__(self) -> str:
        return f'Roteador: {self.ssid}'


class Impressora(models.Model):

    usb = models.BooleanField(verbose_name='Placa USB', default=True, null=False, choices=CHOICES_BOOL)