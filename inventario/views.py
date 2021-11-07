from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import CreateView
from django.views import View

from inventario.forms import GabineteForm, HdForm, MonitorForm, MouseForm, PlacaMaeForm, ProcessadorForm, TecladoForm
from .models import Gabinete, Hd, Monitor, Mouse, PlacaMae, Processador, Teclado
from django.db.models import Q
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required, permission_required



class InventarioView(View):
    
    def get(self, request, *args, **kwargs):
        user = request.user
        parametros = {
            'title': 'Prefeitura de Arapoti',
            'user': user
        }
        return render(request, 'base.html', parametros)

@login_required
@permission_required('inventario.view_mouse', raise_exception=True)
def mouse_view(request, pagina):
    pesquisa = request.GET.get('query')
    mouses = Mouse.objects.filter(Q(computador__isnull=True) | Q(computador__departamento__isnull=True, computador__funcionario__isnull=True))
    if pesquisa != '' and pesquisa is not None:
        mouses = mouses.filter(
            Q(marca__icontains=pesquisa) | Q(usb__icontains=pesquisa) | Q(id__iexact=pesquisa)
        )
    mouses = Paginator(mouses.order_by('id'), 5).get_page(pagina)
    content = {
        'mouses': mouses
    }
    return render(request, template_name='mouse/mouse.html', context=content)


@login_required
@permission_required('inventario.change_mouse', raise_exception=True)
def mouse_edit(request, id):
    """Função responsável por exibir formulário de alteração do mouse."""
    mouse_db = get_object_or_404(Mouse, pk=id)
    form = MouseForm(instance=mouse_db)

    context = {
        'form': form,
        'mensagens': []
    }
    if request.method == 'POST':
        form = MouseForm(request.POST, instance=mouse_db)
        if form.is_valid():
            form.save()
            return redirect(mouse_view, 1)
        else:
                for valores in form.errors.values():
                    context['mensagens'].append(valores)
                    
                context['field_erros'] = form.errors.keys()
    return render(request, 'mouse/editar.html', context=context)

@login_required
@permission_required('inventario.add_mouse', raise_exception=True)
def mouse_add(request):
    form = MouseForm()

    context = {
        'form': form,
        'mensagens': []
    }
    if request.method == 'POST':
        form = MouseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(mouse_view, 1)
        else:
                for valores in form.errors.values():
                    context['mensagens'].append(valores)
                    
                context['field_erros'] = form.errors.keys()
    return render(request, 'mouse/novo.html', context=context)


@login_required
@permission_required('inventario.view_teclado', raise_exception=True)
def teclado_view(request, pagina):
    pesquisa = request.GET.get('query')
    teclados = Teclado.objects.filter(Q(computador__isnull=True) | Q(computador__departamento__isnull=True, computador__funcionario__isnull=True))
    if pesquisa != '' and pesquisa is not None:
        teclados = teclados.filter(
            Q(marca__icontains=pesquisa) | Q(usb__icontains=pesquisa) | Q(id__iexact=pesquisa)
        )
    teclados = Paginator(teclados.order_by('id'), 5).get_page(pagina)
    content = {
        'teclados': teclados
    }
    return render(request, template_name='teclado/teclado.html', context=content)

@login_required
@permission_required('inventario.change_teclado', raise_exception=True)
def teclado_edit(request, id):
    teclado_db = get_object_or_404(Teclado, pk=id)
    form = MouseForm(instance=teclado_db)

    context = {
        'form': form,
        'mensagens': []
    }
    if request.method == 'POST':
        form = MouseForm(request.POST, instance=teclado_db)
        if form.is_valid():
            form.save()
            return redirect(teclado_view, 1)
        else:
                for valores in form.errors.values():
                    context['mensagens'].append(valores)
                    
                context['field_erros'] = form.errors.keys()
    return render(request, 'teclado/editar.html', context=context)

@login_required
@permission_required('inventario.add_teclado', raise_exception=True)
def teclado_add(request):
    form = TecladoForm()

    context = {
        'form': form,
        'mensagens': []
    }
    if request.method == 'POST':
        form = TecladoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(teclado_view, 1)
        else:
                for valores in form.errors.values():
                    context['mensagens'].append(valores)
                    
                context['field_erros'] = form.errors.keys()
    return render(request, 'teclado/novo.html', context=context)


@login_required
@permission_required('inventario.view_mouse', raise_exception=True)
def gabinete_view(request, pagina):
    pesquisa = request.GET.get('query')
    gabinetes = Gabinete.objects.filter(Q(computador__isnull=True) | Q(computador__departamento__isnull=True, computador__funcionario__isnull=True))
    if pesquisa != '' and pesquisa is not None:
        gabinetes = gabinetes.filter(
            Q(patrimonio__icontains=pesquisa) | Q(modelo__icontains=pesquisa) | Q(id__iexact=pesquisa)
        )
    gabinetes = Paginator(gabinetes.order_by('id'), 5).get_page(pagina)
    content = {
        'gabinetes': gabinetes
    }
    return render(request, template_name='gabinete/gabinete.html', context=content)


@login_required
@permission_required('inventario.change_gabinete', raise_exception=True)
def gabinete_edit(request, id):
    gabinete_db = get_object_or_404(Gabinete, pk=id)
    form = GabineteForm(instance=gabinete_db)

    context = {
        'form': form,
        'mensagens': []
    }
    if request.method == 'POST':
        form = GabineteForm(request.POST, instance=gabinete_db)
        if form.is_valid():
            form.save()
            return redirect(gabinete_view, 1)
        else:
                for valores in form.errors.values():
                    context['mensagens'].append(valores)
                    
                context['field_erros'] = form.errors.keys()
    return render(request, 'gabinete/editar.html', context=context)

@login_required
@permission_required('inventario.add_gabinete', raise_exception=True)
def gabinete_add(request):
    form = GabineteForm()

    context = {
        'form': form,
        'mensagens': []
    }
    if request.method == 'POST':
        form = GabineteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(gabinete_view, 1)
        else:
                for valores in form.errors.values():
                    context['mensagens'].append(valores)
                    
                context['field_erros'] = form.errors.keys()
    return render(request, 'gabinete/novo.html', context=context)

@login_required
@permission_required('inventario.view_hd', raise_exception=True)
def hd_view(request, pagina):
    pesquisa = request.GET.get('query')
    hd = Hd.objects.filter(computador__isnull=True)
    if pesquisa != '' and pesquisa is not None:
        hd = hd.filter(
            Q(modelo__icontains=pesquisa) | Q(tamanho_gb__icontains=pesquisa) | Q(id__iexact=pesquisa)
        )
    hd = Paginator(hd.order_by('id'), 5).get_page(pagina)
    content = {
        'hds': hd
    }
    return render(request, template_name='hd/hd.html', context=content)


@login_required
@permission_required('inventario.change_hd', raise_exception=True)
def hd_edit(request, id):
    hd_db = get_object_or_404(Hd, pk=id)
    form = HdForm(instance=hd_db)

    context = {
        'form': form,
        'mensagens': []
    }
    if request.method == 'POST':
        form = HdForm(request.POST, instance=hd_db)
        if form.is_valid():
            form.save()
            return redirect(hd_view, 1)
        else:
                for valores in form.errors.values():
                    context['mensagens'].append(valores)
                    
                context['field_erros'] = form.errors.keys()
    return render(request, 'hd/editar.html', context=context)

@login_required
@permission_required('inventario.add_hd', raise_exception=True)
def hd_add(request):
    form = HdForm()

    context = {
        'form': form,
        'mensagens': []
    }
    if request.method == 'POST':
        form = HdForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(hd_view, 1)
        else:
                for valores in form.errors.values():
                    context['mensagens'].append(valores)
                    
                context['field_erros'] = form.errors.keys()
    return render(request, 'hd/novo.html', context=context)


@login_required
@permission_required('inventario.view_placamae', raise_exception=True)
def placamae_view(request, pagina):
    pesquisa = request.GET.get('query')
    placasmae = PlacaMae.objects.filter(computador__isnull=True)
    if pesquisa != '' and pesquisa is not None:
        placasmae = placasmae.filter(
            Q(marca__icontains=pesquisa) | Q(hdmi__icontains=pesquisa) | Q(modelo__icontains=pesquisa) | Q(processador_suporte__icontains=pesquisa) | Q(id__iexact=pesquisa)
        )
    placasmae = Paginator(placasmae.order_by('id'), 5).get_page(pagina)
    content = {
        'placasmae': placasmae
    }
    return render(request, template_name='placamae/placamae.html', context=content)


@login_required
@permission_required('inventario.change_placamae', raise_exception=True)
def placamae_edit(request, id):
    placamae_db = get_object_or_404(PlacaMae, pk=id)
    form = PlacaMaeForm(instance=placamae_db)

    context = {
        'form': form,
        'mensagens': []
    }
    if request.method == 'POST':
        form = PlacaMaeForm(request.POST, instance=placamae_db)
        if form.is_valid():
            form.save()
            return redirect(placamae_view, 1)
        else:
                for valores in form.errors.values():
                    context['mensagens'].append(valores)
                    
                context['field_erros'] = form.errors.keys()
    return render(request, 'placamae/editar.html', context=context)

@login_required
@permission_required('inventario.add_placamae', raise_exception=True)
def placamae_add(request):
    form = PlacaMaeForm()

    context = {
        'form': form,
        'mensagens': []
    }
    if request.method == 'POST':
        form = PlacaMaeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(placamae_view, 1)
        else:
                for valores in form.errors.values():
                    context['mensagens'].append(valores)
                    
                context['field_erros'] = form.errors.keys()
    return render(request, 'placamae/novo.html', context=context)

@login_required
@permission_required('inventario.view_processador', raise_exception=True)
def processador_view(request, pagina):
    pesquisa = request.GET.get('query')
    processadores = Processador.objects.filter(computador__isnull=True)
    if pesquisa != '' and pesquisa is not None:
        processadores = processadores.filter(
            Q(marca__icontains=pesquisa) | Q(frequencia__icontains=pesquisa) | Q(modelo__icontains=pesquisa) | Q(memoria_cache__icontains=pesquisa) | Q(id__iexact=pesquisa)
        )
    processadores = Paginator(processadores.order_by('id'), 5).get_page(pagina)
    content = {
        'processadores': processadores
    }
    return render(request, template_name='processador/processador.html', context=content)


@login_required
@permission_required('inventario.change_processador', raise_exception=True)
def processador_edit(request, id):
    processador_db = get_object_or_404(Processador, pk=id)
    form = ProcessadorForm(instance=processador_db)

    context = {
        'form': form,
        'mensagens': []
    }
    if request.method == 'POST':
        form = ProcessadorForm(request.POST, instance=processador_db)
        if form.is_valid():
            form.save()
            return redirect(processador_view, 1)
        else:
                for valores in form.errors.values():
                    context['mensagens'].append(valores)
                    
                context['field_erros'] = form.errors.keys()
    return render(request, 'processador/editar.html', context=context)

@login_required
@permission_required('inventario.add_processador', raise_exception=True)
def processador_add(request):
    form = ProcessadorForm()

    context = {
        'form': form,
        'mensagens': []
    }
    if request.method == 'POST':
        form = ProcessadorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(processador_view, 1)
        else:
                for valores in form.errors.values():
                    context['mensagens'].append(valores)
                    
                context['field_erros'] = form.errors.keys()
    return render(request, 'processador/novo.html', context=context)


@login_required
@permission_required('inventario.view_monitor', raise_exception=True)
def monitor_view(request, pagina):
    pesquisa = request.GET.get('query')
    monitores = Monitor.objects.filter(computador__isnull=True)
    if pesquisa != '' and pesquisa is not None:
        monitores = monitores.filter(
            Q(marca__icontains=pesquisa) | Q(hdmi__icontains=pesquisa) | Q(patrimonio__icontains=pesquisa) | Q(tamanho__icontains=pesquisa) | Q(id__iexact=pesquisa)
        )
    monitores = Paginator(monitores.order_by('id'), 5).get_page(pagina)
    content = {
        'monitores': monitores
    }
    return render(request, template_name='monitor/monitor.html', context=content)


@login_required
@permission_required('inventario.change_monitor', raise_exception=True)
def monitor_edit(request, id):
    monitor_db = get_object_or_404(Monitor, pk=id)
    form = MonitorForm(instance=monitor_db)

    context = {
        'form': form,
        'mensagens': []
    }
    if request.method == 'POST':
        form = MonitorForm(request.POST, instance=monitor_db)
        if form.is_valid():
            form.save()
            return redirect(monitor_view, 1)
        else:
                for valores in form.errors.values():
                    context['mensagens'].append(valores)
                    
                context['field_erros'] = form.errors.keys()
    return render(request, 'monitor/editar.html', context=context)

@login_required
@permission_required('inventario.add_monitor', raise_exception=True)
def monitor_add(request):
    form = MonitorForm()

    context = {
        'form': form,
        'mensagens': []
    }
    if request.method == 'POST':
        form = MonitorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(monitor_view, 1)
        else:
                for valores in form.errors.values():
                    context['mensagens'].append(valores)
                    
                context['field_erros'] = form.errors.keys()
    return render(request, 'monitor/novo.html', context=context)
