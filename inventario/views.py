from django.shortcuts import render
from django.views.generic import CreateView
from django.views import View


class InventarioView(View):
    
    def get(self, request, *args, **kwargs):
        user = request.user
        parametros = {
            'title': 'Prefeitura de Arapoti',
            'user': user
        }
        return render(request, 'base.html', parametros)