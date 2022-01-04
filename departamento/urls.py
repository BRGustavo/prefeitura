from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.views.generic import TemplateView, RedirectView
from sistema.settings import BASE_DIR
from . import views, ajax

urlpatterns = [
    #URLs Model Departamento
    path('departamento/<int:pagina>/', views.departamento_view, name='departamento'),
    path('departamento/visualizar/<int:id>/', views.departamento_visualizar, name='departamento_visualizar'),
    path('departamento/remover/<int:id>/', views.departamento_remover, name='departamento_remover'),

    #URLs Model Funcionario
    path('funcionario/<int:pagina>/', views.funcionario_view, name='funcionario'),
    path('funcionario/remover/<int:id>/', views.funcionario_remover, name='funcionario_remover'),
    path('funcionari/editarform_ajax/', ajax.funcionario_edit_form_ajax, name='funcionario_edit_form_ajax'),

    #Ajax URL
    path('departamento/ajax/view', ajax.departamento_view_ajax, name='departamento_view_ajax'),
    path('funcionario/ajax/add/',ajax.funcionario_add_ajax, name='funcionario_ajax_add'),
    path('funcionario/ajax/edit/<int:id>',ajax.funcionario_edit_ajax, name='funcionario_ajax_edit'),

    path('departamento/ajax/add/',ajax.departamento_add_ajax, name='departamento_ajax_add'),
    path('departamento/ajax/edit/',ajax.departamento_edit_ajax, name='departamento_ajax_edit'),
    path('departamento/ajax/deletar',ajax.departamento_ajax_deletar, name='departamento_ajax_deletar'),
]