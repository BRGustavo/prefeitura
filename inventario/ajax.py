from django.contrib.auth.decorators import login_required, permission_required

from django.http.response import JsonResponse

from inventario.models import Gabinete
from .forms import GabineteForm, HdForm, MonitorForm, PlacaMaeForm, ProcessadorForm, TecladoForm, MouseForm


# @login_required
# @permission_required('inventario.add_teclado', raise_exception=True)
# def teclado_add_ajax(request):
#     mensagens = []
#     if request.method == 'POST':
#         form = TecladoForm(request.POST)
#         if form.is_valid():
#             data = {}
#             novo_ = form.save()
#             data['id'] = novo_.id
#             data['modelo'] = novo_.marca
#             data['seletor'] = str(novo_)
#             return JsonResponse(data=data, safe=True)
#         else:
#                 for valores in form.errors.values():
#                     mensagens.append(valores)
#     return JsonResponse(status=404, data={'status':'false','messagem': mensagens})


# @login_required
# @permission_required('inventario.add_mouse', raise_exception=True)
# def mouse_add_ajax(request):
#     mensagens = []
#     if request.method == 'POST':
#         form = MouseForm(request.POST)
#         if form.is_valid():
#             data = {}
#             novo_ = form.save()
#             data['id'] = novo_.id
#             data['modelo'] = novo_.marca
#             data['seletor'] = str(novo_)
#             return JsonResponse(data=data, safe=True)
#         else:
#                 for valores in form.errors.values():
#                     mensagens.append(valores)
#     return JsonResponse(status=404, data={'status':'false','messagem': mensagens})

# @login_required
# @permission_required('inventario.add_gabinete', raise_exception=True)
# def gabinete_add_ajax(request):
#     mensagens = []
#     if request.method == 'POST':
#         form = GabineteForm(request.POST)
#         if form.is_valid():
#             data = {}
#             novo_ = form.save()
#             data['id'] = novo_.id
#             data['modelo'] = novo_.modelo
#             data['seletor'] = str(novo_)
#             return JsonResponse(data=data, safe=True)
#         else:
#                 for valores in form.errors.values():
#                     mensagens.append(valores)
#     return JsonResponse(status=404, data={'status':'false','messagem': mensagens})


# @login_required
# @permission_required('inventario.add_hd', raise_exception=True)
# def hd_add_ajax(request):
#     mensagens = []
#     if request.method == 'POST':
#         form = HdForm(request.POST)
#         if form.is_valid():
#             data = {}
#             novo_ = form.save()
#             data['id'] = novo_.id
#             data['modelo'] = novo_.modelo
#             data['seletor'] = str(novo_)
#             return JsonResponse(data=data, safe=True)
#         else:
#                 for valores in form.errors.values():
#                     mensagens.append(valores)
#     return JsonResponse(status=404, data={'status':'false','messagem': mensagens})


# @login_required
# @permission_required('inventario.add_placamae', raise_exception=True)
# def placamae_add_ajax(request):
#     mensagens = []
#     if request.method == 'POST':
#         form = PlacaMaeForm(request.POST)
#         if form.is_valid():
#             data = {}
#             novo_ = form.save()
#             data['id'] = novo_.id
#             data['modelo'] = novo_.modelo
#             data['seletor'] = str(novo_)
#             return JsonResponse(data=data, safe=True)
#         else:
#                 for valores in form.errors.values():
#                     mensagens.append(valores)
#     return JsonResponse(status=404, data={'status':'false','messagem': mensagens})

# @login_required
# @permission_required('inventario.add_processador', raise_exception=True)
# def processador_add_ajax(request):
#     mensagens = []
#     campo_erros = []
    
#     if request.method == 'POST':
#         form = ProcessadorForm(request.POST)
#         if form.is_valid():
#             data = {}
#             novo_ = form.save()
#             data['id'] = novo_.id
#             data['modelo'] = novo_.modelo
#             data['seletor'] = str(novo_)
#             return JsonResponse(data=data, safe=True)
#         else:
#                 for valores in form.errors.values():
#                     mensagens.append(valores)
#                 for campo in form:
#                     if campo.errors:
#                         campo_erros.append(campo.id_for_label)
#                         print(f'{campo.id_for_label}')

#     return JsonResponse(status=404, data={'status':'false','messagem': mensagens, 'campo_erros': campo_erros})

# @login_required
# @permission_required('inventario.add_monitor', raise_exception=True)
# def monitor_add_ajax(request):
#     mensagens = []
#     if request.method == 'POST':
#         form = MonitorForm(request.POST)
#         if form.is_valid():
#             data = {}
#             novo_ = form.save()
#             data['id'] = novo_.id
#             data['modelo'] = novo_.marca
#             data['seletor'] = str(novo_)
#             return JsonResponse(data=data, safe=True)
#         else:
#                 for valores in form.errors.values():
#                     mensagens.append(valores)
#     return JsonResponse(status=404, data={'status':'false','messagem': mensagens})