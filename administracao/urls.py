from django.contrib import admin
from django.views.generic import TemplateView
from django.urls import path
from . import views, ajax


urlpatterns = [
    path('', views.admin_home, name='admin_home'),
    path('usuarios/', views.admin_usuarios, name='admin_usuarios'),

    path('usuario/ajax/removerUsuario/', ajax.remover_usuario_ajax, name='remover_usuario_ajax'),

]
