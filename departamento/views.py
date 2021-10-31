from django.core import paginator
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required, permission_required

import departamento
from .models import Departamento, Funcionario
from .forms import DepartamentoForm, FuncionarioForm
from django.db.models import Q, F
from django.core.paginator import Paginator

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
        'pesquisa': pesquisa
    }
    return render(request, template_name='departamento/departamento.html', context=content)

@login_required
@permission_required('departamento.add_departamento', raise_exception=True)
def departamento_create(request):
    """Função responsável pelo templete de adicionar outro departamento."""
    context = {
        'form': DepartamentoForm(),
        'mensagens': [],
    }
    if request.method == 'POST':
        formulario = DepartamentoForm(request.POST)
        if formulario.is_valid():
            formulario.save()
            return redirect(f'/departamento/departamento')
        else:
                for valores in formulario.errors.values():
                    context['mensagens'].append(valores)
                    
                context['field_erros'] = formulario.errors.keys()

    return render(request, 'departamento/novo.html', context=context)

@login_required
@permission_required('departamento.change_departamento', raise_exception=True)
def departamento_edit(request, id):
    """Função chamada quando o usuário clica em editar o departamento."""
    departamento_db = get_object_or_404(Departamento, pk=id)
    form = DepartamentoForm(instance=departamento_db)

    context = {
        'form': form,
        'mensagens': []
    }
    if request.method == 'POST':
        form = DepartamentoForm(request.POST, instance=departamento_db)
        if form.is_valid():
            form.save()
            return redirect(departamento_view, 1)
        else:
                for valores in form.errors.values():
                    context['mensagens'].append(valores)
                    
                context['field_erros'] = form.errors.keys()
    return render(request, 'departamento/editar.html', context=context)


@login_required
@permission_required('departamento.view_funcionario', raise_exception=True)
def funcionario_view(request, pagina=1):
    """Função responsável pelo template de listar os usuários """
    pesquisa = request.GET.get('query')
    
    funcionarios_lista = Funcionario.objects.all()
    if pesquisa != '' and pesquisa is not None:

        funcionarios_lista = funcionarios_lista.filter(
            Q(nome__icontains=pesquisa) | Q(sobrenome__icontains=pesquisa) | Q(departamento__departamento__icontains=pesquisa) | Q(departamento__predio__icontains=pesquisa) | Q(controle_acesso__icontains=pesquisa) | Q(id__iexact=pesquisa) | Q(usuario_pc__icontains=pesquisa)
        )

    funcionarios = Paginator(funcionarios_lista.order_by('id'), 10).get_page(pagina)

    content = {
        'funcionarios': funcionarios,
        'pesquisa':pesquisa,
    }
    return render(request, template_name='funcionario/funcionario.html', context=content)


@login_required
@permission_required('departamento.add_funcionario', raise_exception=True)
def funcionario_create(request):
    """Função responsável por cuidar da criação de um novo usuário"""
    context = {
        'form': FuncionarioForm,
        'mensagens': []
    }

    if request.method == 'POST':
        formulario = FuncionarioForm(request.POST)
        if formulario.is_valid():
            formulario.save()
            return redirect(funcionario_view, 1)
        else:
                for valores in formulario.errors.values():
                    context['mensagens'].append(valores)
                    
                context['field_erros'] = formulario.errors.keys()
    
    return render(request, 'funcionario/novo.html', context=context)


@login_required
@permission_required('departamento.change_funcionario', raise_exception=True)
def funcionario_edit(request, id):
    """Função responsável por exibir formulário de alteração funcionário."""
    funcionario_db = get_object_or_404(Funcionario, pk=id)
    form = FuncionarioForm(instance=funcionario_db)

    context = {
        'form': form,
        'mensagens': []
    }
    if request.method == 'POST':
        form = FuncionarioForm(request.POST, instance=funcionario_db)
        if form.is_valid():
            form.save()
            return redirect(f'/funcionario/funcionario')
        else:
                for valores in form.errors.values():
                    context['mensagens'].append(valores)
                    
                context['field_erros'] = form.errors.keys()
    return render(request, 'funcionario/editar.html', context=context)
