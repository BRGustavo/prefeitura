# Generated by Django 3.2.8 on 2021-10-21 20:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dispositivo', '0006_auto_20211021_1952'),
    ]

    operations = [
        migrations.AlterField(
            model_name='impressora',
            name='patrimonio',
            field=models.CharField(blank=True, help_text='Número do patrimônio', max_length=50, null=True, verbose_name='Patrimônio'),
        ),
    ]
