# Generated by Django 3.2.8 on 2021-10-21 21:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dispositivo', '0009_rename_parente_conteudo_tipo_enderecoip_content_type'),
    ]

    operations = [
        migrations.RenameField(
            model_name='enderecoip',
            old_name='parente_objeto_id',
            new_name='parent_object_id',
        ),
    ]
