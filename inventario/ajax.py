from django.contrib.auth.decorators import login_required, permission_required

from django.http.response import JsonResponse

from inventario.models import Gabinete
from .forms import GabineteForm, TecladoForm, MouseForm


@login_required
@permission_required('inventario.add_teclado', raise_exception=True)
def teclado_add_ajax(request):
    mensagens = []
    if request.method == 'POST':
        form = TecladoForm(request.POST)
        if form.is_valid():
            data = {}
            novo_ = form.save()
            data['id'] = novo_.id
            data['modelo'] = novo_.marca
            data['seletor'] = str(novo_)
            return JsonResponse(data=data, safe=True)
        else:
                for valores in form.errors.values():
                    mensagens.append(valores)
    return JsonResponse(status=404, data={'status':'false','messagem': mensagens})


@login_required
@permission_required('inventario.add_mouse', raise_exception=True)
def mouse_add_ajax(request):
    mensagens = []
    if request.method == 'POST':
        form = MouseForm(request.POST)
        if form.is_valid():
            data = {}
            novo_ = form.save()
            data['id'] = novo_.id
            data['modelo'] = novo_.marca
            data['seletor'] = str(novo_)
            return JsonResponse(data=data, safe=True)
        else:
                for valores in form.errors.values():
                    mensagens.append(valores)
    return JsonResponse(status=404, data={'status':'false','messagem': mensagens})

@login_required
@permission_required('inventario.add_gabinete', raise_exception=True)
def gabinete_add_ajax(request):
    mensagens = []
    if request.method == 'POST':
        form = GabineteForm(request.POST)
        if form.is_valid():
            data = {}
            novo_ = form.save()
            data['id'] = novo_.id
            data['modelo'] = novo_.modelo
            data['seletor'] = str(novo_)
            return JsonResponse(data=data, safe=True)
        else:
                for valores in form.errors.values():
                    mensagens.append(valores)
    return JsonResponse(status=404, data={'status':'false','messagem': mensagens})