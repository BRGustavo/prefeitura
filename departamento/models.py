from django.db import models
from django.db.models.deletion import CASCADE

class Departamento(models.Model):
    CHOICES_PREDIOS = [
        ('Prefeitura Arapoti', 'Prefeitura Municipal de Arapoti'),
        ('Col. Clotário', 'Colégio Clortário Portugal'),
        ('Col. Tel.Carneiro', 'Colégio Telemaco Carneiro'),
        ('Col. D.Zizi', 'Colégio Dona Zizi'),
        ('UBS Jd.Aratinga', 'UBS Jardim Aratinga'),
        ('UBS Jd.Ceres', 'UBS Jardim Ceres'),
        ('UBS Vila Romana', 'UBS Vila Romana'),
        ('CRAS', 'CRAS'),
        ('CREAS', 'CREAS - Centro de Referência Especializado em Assistência Social')
    ]

    predio = models.CharField(max_length=255, null=False, choices=CHOICES_PREDIOS)
    departamento = models.CharField(max_length=255, null=False)
    singla_departamento = models.CharField(max_length=5, blank=True, null=True)
    descricao = models.TextField(blank=True, null=True)


    def __str__(self) -> str:
        return f'{self.sigla_departamento} - {self.predio}'

    @property
    def sigla_departamento(self) -> str:
        if len(self.singla_departamento) >= 1:
            return self.singla_departamento
        else:
            return self.departamento


class Funcionario(models.Model):
    nome = models.CharField(max_length=255, null=False)
    sobrenome = models.CharField(max_length=255, null=False)
    departamento = models.ForeignKey('Departamento', default='Prefeitura Municipal De Arapoti', null=False, on_delete=CASCADE)
    admin_rede = models.BooleanField(verbose_name='Administrador Rede', default=False, null=False, choices=(
        (True, 'Sim'),
        (False, 'Não')
    ), help_text='Possui privilégios de administrador na rede.')
    usuario_pc = models.CharField(max_length=50, verbose_name="Usuário PC", null=True, blank=True)
    senha_pc = models.CharField(max_length=50, verbose_name='Senha PC', blank=True, null=True)
    controle_acesso = models.CharField(max_length=20, verbose_name='Acesso Proxy', default='Pessimista', choices=[
        ('Pessimista', 'Pessimista'),
        ('Otimista', 'Otimista')
    ],
    help_text='Controle de acesso a sites rede. Pessimista: Controle rígido; Otimista: Pouco controle.')
    descricao = models.TextField(blank=True, null=True)

    def __str__(self) -> str:
        return f'{self.nome} {self.sobrenome} - {self.departamento.sigla_departamento}'
    

