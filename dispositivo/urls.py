from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.views.generic import TemplateView, RedirectView

from sistema.settings import BASE_DIR

urlpatterns = [
    path('computador/', TemplateView.as_view(template_name='base.html'), name='departamento'),
    path('roteador/', TemplateView.as_view(template_name='base.html'), name='funcionario'),
    path('impressora/', TemplateView.as_view(template_name='base.html'), name='impressora')

]