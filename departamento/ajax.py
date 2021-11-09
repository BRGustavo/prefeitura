from django.contrib.auth.decorators import login_required, permission_required

from departamento.models import Funcionario
from .forms import DepartamentoForm, FuncionarioForm
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