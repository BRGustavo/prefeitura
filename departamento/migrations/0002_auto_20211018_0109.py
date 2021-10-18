# Generated by Django 3.2.8 on 2021-10-18 01:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('departamento', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='funcionario',
            name='departamento',
        ),
        migrations.AddField(
            model_name='funcionario',
            name='departamento',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='departamento.departamento'),
            preserve_default=False,
        ),
    ]
