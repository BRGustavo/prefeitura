from django.contrib.auth.decorators import login_required, permission_required

from departamento.models import Funcionario
from .forms import FuncionarioForm
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