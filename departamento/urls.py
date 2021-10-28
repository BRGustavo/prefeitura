from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.views.generic import TemplateView, RedirectView
from sistema.settings import BASE_DIR
from . import views

urlpatterns = [
    path('departamento/', views.departamento_view, name='departamento'),
    path('departamento/add', views.departamento_create, name='departamento_add'),
    path('funcionario/', views.funcionario_view, name='funcionario'),
    path('funcionario/add', views.funcionario_create, name='funcionario_add')
]