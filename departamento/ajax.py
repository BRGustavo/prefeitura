from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import get_object_or_404

from departamento.models import Funcionario
from .forms import DepartamentoForm, FuncionarioForm
from .models import Departamento
from django.http.response import JsonResponse


@login_required
@permission_required('departamento.add_departamento', raise_exception=True)
def funcionario_add_ajax(request):
    mensagens = []
    if request.method == 'POST':
        form = FuncionarioForm(request.POST)
        if form.is_valid():
            data = {}
            novo_funcionario = form.save()
            data['id'] = novo_funcionario.id
            data['nome'] = novo_funcionario.nome
            data['seletor'] = str(novo_funcionario)
            return JsonResponse(data=data, safe=True)
        else:
                for valores in form.errors.values():
                    mensagens.append(valores)
                    
    return JsonResponse(status=404, data={'status':'false','messagem': mensagens})


@login_required
@permission_required('departamento.add_departamento', raise_exception=True)
def departamento_add_ajax(request):
    mensagens = []
    campo_erros = []
    if request.method == 'POST':
        form = DepartamentoForm(request.POST)
        if form.is_valid():
            data = {}
            novo_ = form.save()
            data['id'] = novo_.id
            data['seletor'] = str(novo_)
            return JsonResponse(data=data, safe=True)
        else:
                for valores in form.errors.values():
                    mensagens.append(valores)
                for campo in form:
                    if campo.errors:
                        campo_erros.append(campo.id_for_label)

    return JsonResponse(status=404, data={'status':'false','messagem': mensagens, 'field_erros': campo_erros})

@login_required
@permission_required('departamento.change_departamento', raise_exception=True)
def departamento_edit_ajax(request, id):
    mensagens = []
    campo_erros = []
    departamento = get_object_or_404(Departamento, pk=id)
    if request.method == 'POST':
        form = DepartamentoForm(request.POST, instance=departamento)
        if form.is_valid():
            editado = form.save()
            print(f'{editado.id}')
            return JsonResponse(data={'id': editado.id}, safe=True)
        else:
            for valores in form.errors.values():
                mensagens.append(valores)
            for campo in form:
                if campo.errors:
                    campo_erros.append(campo.id_for_label)
    return JsonResponse(status=404, data={'status':'false','messagem': mensagens, 'field_erros': campo_erros})