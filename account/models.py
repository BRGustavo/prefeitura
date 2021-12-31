from django.contrib.auth.models import AbstractBaseUser, User
from django.db import models
from django.db.models.deletion import CASCADE
from django.db.models.fields.related import OneToOneField


class CustomizadoUserModel(AbstractBaseUser):
    pass


class UsuarioPerfil(models.Model):
    usuario = OneToOneField(User, related_name='UsuarioPerfil', on_delete=CASCADE)
    aniversario = models.DateField(auto_now_add=True, blank=True, null=True)
    nivel = models.CharField(max_length=150, default='Normal', null=True, blank=True)

    def __str__(self) -> str:
        return f'{self.usuario.username} nivel: {self.nivel}'