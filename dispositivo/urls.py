from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.views.generic import TemplateView, RedirectView
from . import views
from . import ajax
from sistema.settings import BASE_DIR

urlpatterns = [
    path('computador/<int:pagina>/', views.computador_view, name='computador'),
    path('computador/add/', views.computador_create, name='computador_add'),
    path('computador/add/ajax', ajax.computador_create_ajax, name='computador_add_ajax'),
    path('roteador/', TemplateView.as_view(template_name='base.html'), name='roteador'),
    path('impressora/', TemplateView.as_view(template_name='base.html'), name='impressora')

]