from django.contrib import admin
from django.views.generic import TemplateView
from .views import InventarioView
from django.urls import path


urlpatterns = [
    path('', InventarioView.as_view(), name='inventario_criar'),
    
]
