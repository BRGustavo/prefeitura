# Generated by Django 3.2.8 on 2021-10-19 21:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dispositivo', '0003_auto_20211019_2132'),
    ]

    operations = [
        migrations.AddField(
            model_name='impressora',
            name='gestpar_matricula',
            field=models.CharField(max_length=20, null=True),
        ),
    ]
