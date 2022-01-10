from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import CreateView
from django.views import View

from inventario.forms import GabineteForm, HdForm, MonitorForm, MouseForm, PlacaMaeForm, ProcessadorForm, TecladoForm
from .models import Gabinete, Hd, Monitor, Mouse, PlacaMae, Processador, Teclado
from django.db.models import Q
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required, permission_required



class InventarioView(View):
    
    def get(self, request, *args, **kwargs):
        user = request.user
        parametros = {
            'title': 'Prefeitura de Arapoti',
            'user': user
        }
        return render(request, 'base.html', parametros)
