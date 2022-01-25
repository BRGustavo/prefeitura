from django.contrib import admin
from django.views.generic import TemplateView
# from .views import InventarioView
from django.urls import path
from . import ajax


urlpatterns = [
    #Ajax URL
    # path('teclado/ajax/add/',ajax.teclado_add_ajax, name='teclado_ajax_add'),
    # path('mouse/ajax/add/',ajax.mouse_add_ajax, name='mouse_ajax_add'),
    # path('gabinete/ajax/add/',ajax.gabinete_add_ajax, name='gabinete_ajax_add'),
    # path('processador/ajax/add/',ajax.processador_add_ajax, name='processador_ajax_add'),
    # path('placamae/ajax/add/',ajax.placamae_add_ajax, name='placamae_ajax_add'),
    # path('monitor/ajax/add/',ajax.monitor_add_ajax, name='monitor_ajax_add'),
    # path('hd/ajax/add/',ajax.hd_add_ajax, name='hd_ajax_add'),
]
