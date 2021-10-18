from django.db import models
from django.db.models.deletion import CASCADE

class Departamento(models.Model):
    CHOICES_PREDIOS = [
        ('Prefeitura Municipal De Arapoti', 'Prefeitura Municipal de Arapoti'),
        ('Col. Clotário Portual', 'Colégio Clortário Portugal'),
        ('Col. Telemaco Carneiro', 'Colégio Telemaco Carneiro'),
        ('Col. Dona Zizi', 'Colégio Dona Zizi'),
        ('UBS Jardim Aratinga', 'UBS Jardim Aratinga'),
        ('UBS Jardim Ceres', 'UBS Jardim Ceres'),
        ('UBS Vila Romana', 'UBS Vila Romana'),
        ('CREAS', 'CREAS'),
        ('CREAS', 'CREAS - Centro de Referência Especializado em Assistência Social')
    ]

    predio = models.CharField(max_length=255, null=False, choices=CHOICES_PREDIOS)
    departamento = models.CharField(max_length=255, null=False)
    singla_departamento = models.CharField(max_length=5, blank=True, null=True)
    descricao = models.TextField(blank=True, null=True)


    def __str__(self) -> str:
        return f'Departamento: {self.departamento} Predio: {self.predio}'


class Funcionario(models.Model):
    nome = models.CharField(max_length=255, null=False)
    sobrenome = models.CharField(max_length=255, null=False)
    departamento = models.ForeignKey('Departamento', default='Prefeitura Municipal De Arapoti', null=False, on_delete=CASCADE)
    sexo = models.CharField(max_length=1, default='M', null=False, choices=(('M', 'Masculino'), ('F', 'Feminino')))
    usuario_pc = models.CharField(max_length=50, verbose_name="Usuário PC", null=True, blank=True)
    senha_pc = models.CharField(max_length=50, verbose_name='Senha PC', blank=True, null=True)
    controle_acesso = models.CharField(max_length=20, verbose_name='Acesso Proxy', default='Pessimista', choices=[
        ('Pessimista', 'Pessimista'),
        ('Otimista', 'Otimista')
    ],
    help_text='Controle de acesso a sites rede. Pessimista: Controle rígido; Otimista: Pouco controle.')
    descricao = models.TextField(blank=True, null=True)

    def __str__(self) -> str:
        return f'{self.nome} {self.sobrenome} {self.departamento.departamento}'
    

