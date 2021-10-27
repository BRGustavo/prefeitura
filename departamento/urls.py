from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.views.generic import TemplateView, RedirectView
from sistema.settings import BASE_DIR
from . import views

urlpatterns = [
    path('departamento/', views.departamento, name='departamento'),
    path('departamento/add', views.departamento_insert, name='departamento insert'),
    path('funcionario/', views.funcionario, name='funcionario')
]