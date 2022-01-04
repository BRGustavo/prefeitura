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
    path('computador/remover/', views.computador_remover, name='computador_remover'),

    # URLs Model Roteador
    path('roteador/<int:pagina>/', views.roteador_view, name='roteador_view'),
    path('roteador/add/', views.roteador_add, name='roteador_add'),
    path('roteador/edit/', views.roteador_edit, name='roteador_edit'),
    path('roteador/ajax/apagarroteador', views.roteador_delete, name='roteador_delete'),

    # URLs Model Impressora
    path('impressora/<int:pagina>/', views.impressora_view, name='impressora_view'),
    path('impressora/ajax/apagarimpressora', views.impressora_delete, name='impressora_delete'),

    # Ajax
    path('computador/add/ajax', ajax.computador_create_ajax, name='computador_add_ajax'),
    path('ip/verificador/ajax/', ajax.verificar_ip_ajax, name='verificar_ip_ajax'),
    path('ip/verificardorip/ajax', ajax.verificar_endereco_ip,name='verificar_enderecoip_ajax'),
    path('impressora/pesquisar/ajax/', ajax.impressora_pesquisa_ajax, name='impressora_pesquisa_ajax'),
    path('impressora/vincular/ajax/', ajax.vincular_impressora_ajax, name='vincular_impressora_ajax'),
    path('computador/atualizarinfo/ajax', ajax.atualizar_computador_info_ajax, name='atualizar_computador_info_ajax'),
    path('computador/atualizarprocessador/ajax/', ajax.atualizar_processador_ajax, name='atualizar_processador_ajax'),
    path('computador/apagar_processador_ajax/ajax/', ajax.deletar_processador_ajax, name='deletar_processador_ajax'),
    path('computador/apagar_placamae_ajax/ajax/', ajax.deletar_placamae_ajax, name='deletar_placamae_ajax'),
    path('computador/atualizarplacamae/ajax/', ajax.atualizar_placamae_ajax, name='atualizar_placamae_ajax'),
    path('computador/computador_novo_ajax/ajax/', ajax.computador_novo_ajax, name='computador_novo_ajax'),
    path('impressora/impressora_nova_ajax/ajax/', ajax.impressora_nova_ajax, name='impressora_nova_ajax'),
    path('impressora/impressora_atualizar_ajax/ajax/', ajax.impressora_atualizar_ajax, name='impressora_atualizar_ajax'),
    path('funcionario/pesquisar/ajax/', ajax.funcionario_pesquisa_ajax, name='funcionario_pesquisa_ajax'),
    path('funcionario/vincular/ajax/', ajax.vincular_funcionario_ajax, name='vincular_funcionario_ajax'),
    path('impressora/impressora_computadores_ajax/ajax/', ajax.view_pc_na_impressora, name='view_pc_na_impressora'),

    path('',views.teste_view, name='teste'),

    # URL Patrimônio
    path('patrimonio/pesquisa/', views.patrimonio_view, name='patrimonio_view'),
    path('agulha/', views.pesquisar_endereco_ip, name='pesquisar_endereco_ip'),
    path('agula/ajax_salvar_reservado/', ajax.salvar_ip_reservado, name='salvar_ip_reservado'),
    path('agula/ajax_removerip_reservado/', ajax.remover_ip_reservado, name='remover_ip_reservado'),
]