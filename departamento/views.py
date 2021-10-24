from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required, permission_required
from .models import Departamento
from .forms import DepartamentoForm


@login_required
@permission_required('departamento.view_departamento', raise_exception=True)
def departamento(request):
    departamentos = Departamento.objects.all()
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

    return render(request, 'departamento/novo_departamento.html', context=context)