from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required, permission_required
from .models import Departamento, Funcionario
from .forms import DepartamentoForm, FuncionarioForm
from django.db.models import Q, F


@login_required
@permission_required('departamento.view_departamento', raise_exception=True)
def departamento_view(request):
    pesquisa = request.GET.get('query')
    departamentos = Departamento.objects.all()
    if pesquisa != '' and pesquisa is not None:
        departamentos = departamentos.filter(
            Q(departamento__icontains=pesquisa) | Q(predio__icontains=pesquisa) | Q(singla_departamento__icontains=pesquisa) | Q(id__iexact=pesquisa)
        )
    content = {
        'departamentos': departamentos
    }
    return render(request, template_name='departamento/departamento.html', context=content)

@login_required
@permission_required('departamento.add_departamento', raise_exception=True)
def departamento_create(request):
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
            return redirect(f'/departamento/departamento')
        else:
                for valores in form.errors.values():
                    context['mensagens'].append(valores)
                    
                context['field_erros'] = form.errors.keys()
    return render(request, 'departamento/editar.html', context=context)


@login_required
@permission_required('departamento.view_funcionario', raise_exception=True)
def funcionario_view(request):
    pesquisa = request.GET.get('query')
    funcionarios = Funcionario.objects.all()
    if pesquisa != '' and pesquisa is not None:
        funcionarios = funcionarios.filter(
            Q(nome__icontains=pesquisa) | Q(sobrenome__icontains=pesquisa) | Q(departamento__departamento__icontains=pesquisa) | Q(departamento__predio__icontains=pesquisa) | Q(controle_acesso__icontains=pesquisa) | Q(id__iexact=pesquisa) | Q(usuario_pc__icontains=pesquisa)
        )
    content = {
        'funcionarios': funcionarios
    }
    return render(request, template_name='funcionario/funcionario.html', context=content)


@login_required
@permission_required('departamento.add_funcionario', raise_exception=True)
def funcionario_create(request):
    context = {
        'form': FuncionarioForm,
        'mensagens': []
    }

    if request.method == 'POST':
        formulario = FuncionarioForm(request.POST)
        if formulario.is_valid():
            formulario.save()
            return redirect('/departamento/funcionario')
        else:
                for valores in formulario.errors.values():
                    context['mensagens'].append(valores)
                    
                context['field_erros'] = formulario.errors.keys()
    
    return render(request, 'funcionario/novo.html', context=context)


@login_required
@permission_required('departamento.change_funcionario', raise_exception=True)
def funcionario_edit(request, id):
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
