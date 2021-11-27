from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.views.generic import TemplateView, RedirectView
from . import views
from . import ajax
from sistema.settings import BASE_DIR

urlpatterns = [
    # URLs Model Computador
    path('computador/<int:pagina>/', views.computador_view, name='computador'),
    path('computador/add/', views.computador_create, name='computador_add'),
    path('computador/edit/<int:id>/', views.computador_edit, name='computador_edit'),
    path('computador/visualizar/<int:id>/<str:pagina>/', views.computador_visualizar, name='computador_visualizar'),

    # URLs Model Roteador
    path('roteador/<int:pagina>/', views.roteador_view, name='roteador_view'),
    path('roteador/add/', views.roteador_add, name='roteador_add'),
    path('roteador/edit/<int:id>/', views.roteador_edit, name='roteador_edit'),

    # URLs Model Impressora
    path('impressora/<int:pagina>/', views.impressora_view, name='impressora_view'),
    path('impressora/edit/<int:id>/', views.impressora_edit, name='impressora_edit'),

    # Ajax
    path('computador/add/ajax', ajax.computador_create_ajax, name='computador_add_ajax'),
    path('ip/verificador/ajax/', ajax.verificar_ip_ajax, name='verificar_ip_ajax'),
    path('ip/verificardorip/ajax', ajax.verificar_endereco_ip,name='verificar_enderecoip_ajax'),
    path('impressora/pesquisar/ajax/', ajax.impressora_pesquisa_ajax, name='impressora_pesquisa_ajax'),
    path('impressora/vincular/ajax/', ajax.vincular_impressora_ajax, name='vincular_impressora_ajax'),
    path('computador/atualizarinfo/ajax', ajax.atualizar_computador_info_ajax, name='atualizar_computador_info_ajax'),
    path('computador/atualizarprocessador/ajax/', ajax.atualizar_processador_ajax, name='atualizar_processador_ajax'),
    path('computador/computador_novo_ajax/ajax/', ajax.computador_novo_ajax, name='computador_novo_ajax'),
    path('impressora/impressora_nova_ajax/ajax/', ajax.impressora_nova_ajax, name='impressora_nova_ajax'),
    path('impressora/impressora_atualizar_ajax/ajax/', ajax.impressora_atualizar_ajax, name='impressora_atualizar_ajax'),

    path('',views.teste_view, name='teste')

]