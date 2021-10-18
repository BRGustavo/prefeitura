# Generated by Django 3.2.8 on 2021-10-18 22:02

from django.db import migrations, models
import django.db.models.deletion
import macaddress.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('departamento', '0006_alter_funcionario_controle_acesso'),
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Impressora',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('usb', models.BooleanField(choices=[(True, 'Sim'), (False, 'Não')], default=True, verbose_name='Placa USB')),
            ],
        ),
        migrations.CreateModel(
            name='Roteador',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ssid', models.CharField(help_text='Nome visivel da rede.', max_length=100, verbose_name='SSID')),
                ('senha', models.CharField(blank=True, max_length=100, null=True)),
                ('modelo', models.CharField(choices=[('TP-LINK', 'TP-Link'), ('D-Link', 'D-Link'), ('Huawei', 'Huawei'), ('Outro', 'Outro')], max_length=50)),
                ('multimodo', models.CharField(choices=[('N', 'Não'), ('S', 'Sim')], default='N', help_text='Multimodo: Frequência 2.4Ghz e 5Ghz.', max_length=1)),
                ('descricao', models.TextField(blank=True, verbose_name='Descrição')),
                ('departamento', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='departamento.departamento')),
            ],
        ),
        migrations.CreateModel(
            name='EnderecoMac',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mac_address', macaddress.fields.MACAddressField(blank=True, integer=True, null=True, unique=True)),
                ('parent_object_id', models.PositiveIntegerField()),
                ('parent_content_type', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='mac_parente', to='contenttypes.contenttype')),
            ],
        ),
        migrations.CreateModel(
            name='EnderecoIp',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ip_address', models.GenericIPAddressField(blank=True, null=True, unique=True, verbose_name='Endereço IP')),
                ('parente_objeto_id', models.PositiveIntegerField()),
                ('parente_conteudo_tipo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ip_parente', to='contenttypes.contenttype')),
            ],
        ),
    ]
