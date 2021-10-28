from django.contrib import admin
from django.views.generic import TemplateView
from .views import InventarioView
from django.urls import path


urlpatterns = [
    path('', InventarioView.as_view(), name='inventario_criar'),
    path('gabinete', TemplateView.as_view(template_name='base.html'), name='gabinete'),
    path('processador', TemplateView.as_view(template_name='base.html'), name='processador'),
    path('teclado', TemplateView.as_view(template_name='base.html'), name='teclado'),
    path('mouse', TemplateView.as_view(template_name='base.html'), name='mouse'),
    path('placamae', TemplateView.as_view(template_name='base.html'), name='placamae'),
    path('fonte', TemplateView.as_view(template_name='base.html'), name='fonte'),
    path('hd', TemplateView.as_view(template_name='base.html'), name='hd'),

]
