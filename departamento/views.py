from django.core import paginator
from django.http.response import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required, permission_required

import departamento
from .models import Departamento, Funcionario
from .forms import DepartamentoForm, FuncionarioForm, FuncionarioVisualizarForm
from django.db.models import Q, F
from django.core.paginator import Paginator
from dispositivo.models import Computador, Impressora, Roteador

@login_required
@permission_required('departamento.view_departamento', raise_exception=True)
def departamento_view(request, pagina=1):
    """Função Responsavel pelo template de listar os departamentos. """
    pesquisa = request.GET.get('query')
    departamentos_list = Departamento.objects.all()
    if pesquisa != '' and pesquisa is not None:
        departamentos_list = departamentos_list.filter(
            Q(departamento__icontains=pesquisa) | Q(predio__icontains=pesquisa) | Q(singla_departamento__icontains=pesquisa) | Q(id__iexact=pesquisa)
        )
    departamentos = Paginator(departamentos_list.order_by('id'), 10).get_page(pagina)
    content = {
        'departamentos': departamentos,
        'pesquisa': pesquisa,
        'form': DepartamentoForm
    }
    return render(request, template_name='departamento/departamento.html', context=content)

@login_required
@permission_required('departamento.view_departamento', raise_exception=True)
def departamento_visualizar(request, id):
    departamento = get_object_or_404(Departamento, pk=id)
    form = DepartamentoForm(instance=departamento)
    impressoras = Impressora.objects.filter(departamento=departamento)
    funcionarios = Funcionario.objects.filter(departamento=departamento)
    computadores = Computador.objects.filter(Q(departamento=departamento, funcionario__isnull=True) | Q(funcionario__in=funcionarios))

    context = {
        'form': form,
        'departamento': departamento,
        'funcionarios': funcionarios,
        'impressoras': impressoras,
        'computadores': computadores
    }
    return render(request, template_name='departamento/visualizar.html', context=context)


@login_required
@permission_required('departamento.delete_departamento', raise_exception=True)
def departamento_remover(request, id):
    departamento = get_object_or_404(Departamento, pk=id)
    funcionarios = Funcionario.objects.all().filter(departamento=departamento)
    impressoras = Impressora.objects.all().filter(departamento=departamento).delete()
    roteadores = Roteador.objects.all().filter(departamento=departamento).delete()
    computadores = Computador.objects.all().filter(Q(departamento=departamento, funcionario__isnull=True) | Q(funcionario__in=funcionarios)).delete()
    funcionarios.delete()
    departamento.delete()
    return redirect(departamento_view, 1)

@login_required
@permission_required('departamento.view_funcionario', raise_exception=True)
def funcionario_view(request, pagina=1):
    """Função responsável pelo template de listar os usuários """
    pesquisa = request.GET.get('query')
    formFuncionario = FuncionarioForm()
    funcionarios_lista = Funcionario.objects.all()
    if pesquisa != '' and pesquisa is not None:

        funcionarios_lista = funcionarios_lista.filter(
            Q(nome__icontains=pesquisa) | Q(sobrenome__icontains=pesquisa) | Q(departamento__departamento__icontains=pesquisa) | Q(departamento__predio__icontains=pesquisa) | Q(controle_acesso__icontains=pesquisa) | Q(id__iexact=pesquisa) | Q(usuario_pc__icontains=pesquisa)
        )

    funcionarios = Paginator(funcionarios_lista.order_by('id'), 15).get_page(pagina)

    content = {
        'funcionarios': funcionarios,
        'pesquisa':pesquisa,
        'formFuncionario': formFuncionario,

    }
    return render(request, template_name='funcionario/funcionario.html', context=content)

@login_required
@permission_required('departamento.view_funcionario', raise_exception=True)
def funcionario_visualizar(request, id=1):
    funcionario = get_object_or_404(Funcionario, pk=id)
    form = FuncionarioForm(instance=funcionario)
    computadores = Computador.objects.filter(funcionario=funcionario)

    context = {
        'form': form,
        'funcionario': funcionario,
        'computadores': computadores,
    }
    return render(request, template_name='funcionario/visualizar.html', context=context)

@login_required
@permission_required('departamento.delete_funcionario')
def funcionario_remover(request, id):
    funcionario = get_object_or_404(Funcionario, pk=id)
    Computador.objects.all().filter(funcionario=funcionario).delete()
    funcionario.delete()
    return redirect(funcionario_view, 1)
