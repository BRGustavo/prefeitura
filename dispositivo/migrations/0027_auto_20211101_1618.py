# Generated by Django 3.2.8 on 2021-11-01 19:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dispositivo', '0026_remove_impressora_patrimonio'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='computador',
            name='patrimonio',
        ),
        migrations.AddField(
            model_name='impressora',
            name='patrimonio',
            field=models.CharField(blank=True, help_text='Número do patrimônio', max_length=50, null=True, verbose_name='Patrimônio'),
        ),
    ]
