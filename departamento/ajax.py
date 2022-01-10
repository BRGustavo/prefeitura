from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import get_object_or_404, redirect
from django.urls.base import reverse

from departamento.models import Funcionario
from departamento.views import departamento_view
from .forms import DepartamentoForm, FuncionarioForm
from .models import Departamento
from django.http.response import JsonResponse
from dispositivo.models import Computador, Roteador, Impressora
from django.db.models import Q


@login_required
@permission_required('departamento.add_departamento', raise_exception=True)
def funcionario_add_ajax(request):
    mensagens = []
    campo_erros = []
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
                for campo in form:
                    if campo.errors:
                        campo_erros.append(campo.id_for_label)
                    
    return JsonResponse(status=404, data={'status':'false','messagem': mensagens, 'field_erros': campo_erros})

@login_required
@permission_required('departamento.change_funcionario', raise_exception=True)
def funcionario_edit_ajax(request, id):
    mensagens = []
    campo_erros = []
    funcionario = get_object_or_404(Funcionario, pk=id)
    if request.method == 'POST':
        form = FuncionarioForm(request.POST, instance=funcionario)
        if form.is_valid():
            editado = form.save()
            return JsonResponse(data={'id': editado.id}, safe=True)
        else:
            for valores in form.errors.values():
                mensagens.append(valores)
            for campo in form:
                if campo.errors:
                    campo_erros.append(campo.id_for_label)
            
    return JsonResponse(status=404, data={'status':'false','messagem': mensagens, 'field_erros': campo_erros})

def funcionario_edit_form_ajax(request):
    if request.method == 'GET':
        if request.is_ajax():
            id_funcionario = request.GET.get('id')
            funcionario = get_object_or_404(Funcionario, pk=id_funcionario)
            departamentos = Departamento.objects.all()
            
            url_atualizar = reverse(funcionario_edit_ajax, args=[funcionario.id])
            lista_departamentos = [{
                'id': dep.id,
                'valor': dep.departamento
            } for dep in departamentos]

            return JsonResponse(status=200, data={
                'id_nome': funcionario.nome,
                'id_sobrenome': funcionario.sobrenome,
                'id_usuario_pc': funcionario.usuario_pc,
                'id_senha_pc': funcionario.senha_pc,
                'id_controle_acesso': funcionario.controle_acesso,
                'id_adm_rede': funcionario.admin_rede,
                'id_descricao': funcionario.descricao,
                'departamentos': lista_departamentos,
                'departamento': funcionario.departamento.id,
                'url': f'UpdateFuncionario("{url_atualizar}")'
            }, safe=True)
    return JsonResponse(status=400, data={'mensagem': 'problema'}, safe=True)

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
def departamento_view_ajax(request):
    if request.method == 'GET':
        id = request.GET.get('id')
        departamento = get_object_or_404(Departamento, id=id)
        if departamento:
            data = {
                'predio': departamento.predio,
                'departamento': departamento.departamento,
                'sigla': departamento.sigla_departamento,
                'descricao': departamento.descricao
            }
            return JsonResponse(status=200, data=data, safe=True)
        else:
            return JsonResponse(status=404, data={'status':False}, safe=True)

@login_required
@permission_required('departamento.change_departamento', raise_exception=True)
def departamento_edit_ajax(request):
    mensagens = []
    campo_erros = []

    if request.method == 'GET':
        id = request.GET.get('id')
        departamento = get_object_or_404(Departamento, id=id)
        if departamento:
            form = DepartamentoForm(request.GET, instance=departamento)
            if form.is_valid():
                form.save()
                return JsonResponse(status=200, data={'status':True}, safe=True)
            else:
                for valores in form.errors.values():
                    mensagens.append(valores)
                for campo in form:
                    if campo.errors:
                        campo_erros.append(campo.id_for_label)
        else:
            mensagens.append('Não foi possivel localizar esse departamento.')
            campo_erros.append(f for f in ['id_predio', 'id_departamento', 'id_descricao'])
    return JsonResponse(status=404, data={'status':'false','messagem': mensagens, 'field_erros': campo_erros})
    

@login_required
@permission_required('departamento.view_departamento', raise_exception=True)
def departamento_ajax_deletar(request):
    data = {}
    campo_erros = []
    if request.method == 'GET':

        departamento = get_object_or_404(Departamento, pk=request.GET.get('id'))
        funcionarios = Funcionario.objects.all().filter(departamento=departamento)
        computadores = Computador.objects.all().filter(Q(departamento=departamento) | Q(funcionario__in=funcionarios))
        roteadores = Roteador.objects.all().filter(departamento=departamento)
        impressoras = Impressora.objects.all().filter(departamento=departamento)

        data = {
            'funcionarios': funcionarios.count(),
            'computadores': computadores.count(),
            'roteadores': roteadores.count(),
            'impressoras': impressoras.count()
        }
        return JsonResponse(data=data, status=200)

    return JsonResponse(status=404, data={'status':'false','field_erros': campo_erros})

    
