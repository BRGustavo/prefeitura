# Generated by Django 3.2.8 on 2021-10-27 22:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dispositivo', '0018_computador_nome_rede'),
    ]

    operations = [
        migrations.AddField(
            model_name='computador',
            name='patrimonio',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Patrimônio'),
        ),
    ]