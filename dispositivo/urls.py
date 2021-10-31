from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.views.generic import TemplateView, RedirectView
from . import views
from sistema.settings import BASE_DIR

urlpatterns = [
    path('computador/', views.computador, name='computador'),
    path('computador/add/', views.computador_create, name='computador_add'),
    path('roteador/', TemplateView.as_view(template_name='base.html'), name='roteador'),
    path('impressora/', TemplateView.as_view(template_name='base.html'), name='impressora')

]