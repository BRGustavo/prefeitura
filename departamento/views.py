from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required, permission_required
from .models import Departamento, Funcionario
from .forms import DepartamentoForm
from django.db.models import Q, F


@login_required
@permission_required('departamento.view_departamento', raise_exception=True)
def departamento(request):
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
def departamento_insert(request):
    context = {
        'form': DepartamentoForm(),
        'mensagens': []
    }
    if request.method == 'POST':
        formulario = DepartamentoForm(request.POST)
        if formulario.is_valid():
            formulario.save()
            return redirect(f'/departamento/departamento')
        else:

            context['mensagens'].append('Você fez alguma mrd, tente de novo!')

    return render(request, 'departamento/novo.html', context=context)

@login_required
@permission_required('departamento.view_funcionario', raise_exception=True)
def funcionario(request):
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
