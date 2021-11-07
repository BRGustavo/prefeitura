from django.contrib import admin
from django.views.generic import TemplateView
from .views import InventarioView
from django.urls import path
from . import ajax, views


urlpatterns = [
    path('', InventarioView.as_view(), name='inventario_criar'),
    path('gabinete', TemplateView.as_view(template_name='base.html'), name='gabinete'),
    path('processador', TemplateView.as_view(template_name='base.html'), name='processador'),
    path('teclado', TemplateView.as_view(template_name='base.html'), name='teclado'),
    path('placamae', TemplateView.as_view(template_name='base.html'), name='placamae'),
    path('fonte', TemplateView.as_view(template_name='base.html'), name='fonte'),
    path('hd', TemplateView.as_view(template_name='base.html'), name='hd'),

    # Mouse URLs
    path('mouse/add/', views.mouse_add, name='mouse_add'),
    path('mouse/<int:pagina>/', views.mouse_view, name='mouse_view'),
    path('mouse/edit/<int:id>', views.mouse_edit, name='mouse_edit'),

    # Teclado URLs
    path('teclado/add/', views.teclado_add, name='teclado_add'),
    path('teclado/<int:pagina>/', views.teclado_view, name='teclado_view'),
    path('teclado/edit/<int:id>', views.teclado_edit, name='teclado_edit'),

    # Gabinete URLs
    path('gabinete/add/', views.gabinete_add, name='gabinete_add'),
    path('gabinete/<int:pagina>/', views.gabinete_view, name='gabinete_view'),
    path('gabinete/edit/<int:id>/', views.gabinete_edit, name='gabinete_edit'),
 
     # Hds URLs
    path('hd/add/', views.hd_add, name='hd_add'),
    path('hd/<int:pagina>/', views.hd_view, name='hd_view'),
    path('hd/edit/<int:id>/', views.hd_edit, name='hd_edit'),

     # Placa Mãe URLs
    path('placamae/add/', views.placamae_add, name='placamae_add'),
    path('placamae/<int:pagina>/', views.placamae_view, name='placamae_view'),
    path('placamae/edit/<int:id>/', views.placamae_edit, name='placamae_edit'),

     # Processador URLs
    path('processador/add/', views.processador_add, name='processador_add'),
    path('processador/<int:pagina>/', views.processador_view, name='processador_view'),
    path('processador/edit/<int:id>/', views.processador_edit, name='processador_edit'),

     # Monitor URLs
    path('monitor/add/', views.monitor_add, name='monitor_add'),
    path('monitor/<int:pagina>/', views.monitor_view, name='monitor_view'),
    path('monitor/edit/<int:id>/', views.monitor_edit, name='monitor_edit'),


    #Ajax URL
    path('teclado/ajax/add/',ajax.teclado_add_ajax, name='teclado_ajax_add'),
    path('mouse/ajax/add/',ajax.mouse_add_ajax, name='mouse_ajax_add'),
    path('gabinete/ajax/add/',ajax.gabinete_add_ajax, name='gabinete_ajax_add'),
    path('processador/ajax/add/',ajax.processador_add_ajax, name='processador_ajax_add'),
    path('placamae/ajax/add/',ajax.placamae_add_ajax, name='placamae_ajax_add'),
    path('monitor/ajax/add/',ajax.monitor_add_ajax, name='monitor_ajax_add'),
    path('hd/ajax/add/',ajax.hd_add_ajax, name='hd_ajax_add'),
]
