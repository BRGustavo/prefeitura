from django.db import models
from django.db.models.deletion import CASCADE
from departamento.models import Departamento

class Roteador(models.Model):

    ssid = models.CharField(max_length=100, null=False)
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
    descricao = models.TextField(blank=True)

    def __str__(self) -> str:
        return f'SSID: {self.ssid} Modelo: {self.modelo}'