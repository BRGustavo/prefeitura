from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required, permission_required
from .models import Computador
from .forms import ComputadorForm
from django.db.models import Q, F


@login_required
@permission_required('dispositivo.view_computador', raise_exception=True)
def computador(request):
    pesquisa = request.GET.get('query')
    computadores = Computador.objects.all()
    if pesquisa != '' and pesquisa is not None:
        computadores = computadores.filter(
            Q(sistema_op__icontains=pesquisa) | Q(funcionario__nome__icontains=pesquisa) | Q(departamento__departamento__icontains=pesquisa) | Q(processador__modelo__icontains=pesquisa) | Q(id__iexact=pesquisa)
        )
    content = {
        'computadores': computadores
    }


    return render(request, template_name='computador/computador.html', context=content)


@login_required
@permission_required('departamento.add_departamento', raise_exception=True)
def computador_create(request):
    form = ComputadorForm()
    context = {
        'form': form,
        'mensagens': []
    }
    if request.method == 'POST':
        form = ComputadorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(f'/dispositivo/computadores')
        else:
                for valores in form.errors.values():
                    context['mensagens'].append(valores)
                    
                context['field_erros'] = form.errors.keys()
    return render(request, template_name='computador/novo.html', context=context)
