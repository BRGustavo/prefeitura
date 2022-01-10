from django.contrib import admin
from django.views.generic import TemplateView
from django.urls import path
from . import views, ajax


urlpatterns = [
    path('', views.admin_home, name='admin_home'),
    path('usuarios/', views.admin_usuarios, name='admin_usuarios'),
    path('permissoes/', views.admin_permissoes, name='admin_permissoes'),
    
    path('usuario/ajax/adicionarUsuario/', ajax.adicionar_usuario_ajax, name='adicionar_usuario_ajax'),
    path('usuario/ajax/removerUsuario/', ajax.remover_usuario_ajax, name='remover_usuario_ajax'),
    path('usuario/ajax/dados_usuario_ajax', ajax.dados_usuario_ajax, name='dados_usuario_ajax'),
    path('usuario/ajax/editar_usuario_ajax', ajax.editar_usuario_ajax, name='editar_usuario_ajax'),

]
