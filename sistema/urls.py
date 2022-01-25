from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.views.generic import TemplateView, RedirectView

from sistema.settings import BASE_DIR

from account.views import index as home_index

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('accounts/', include('account.urls')),
    path('departamento/', include('departamento.urls')),
    path('dispositivo/', include('dispositivo.urls')),
    path('inventario/', include('inventario.urls')),
    path('administracao/', include('administracao.urls')),
    path('', home_index, name='home'),

]