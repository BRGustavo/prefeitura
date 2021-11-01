from django.core.paginator import Paginator
from django.http.response import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required, permission_required
from django.forms import inlineformset_factory
from departamento.models import Funcionario
from .models import Computador, EnderecoIp, EnderecoMac, MemoriaRam, Roteador
from .forms import ComputadorForm, EndereoIpForm, MemoriaRamForm
from django.contrib.contenttypes.models import ContentType
from django.db.models import Q, F
from utils import VerificarIp, VerificarMac


@login_required
@permission_required('dispositivo.view_computador', raise_exception=True)
def computador_view(request, pagina):
    pesquisa = request.GET.get('query')
    computadores = Computador.objects.all()
    if pesquisa != '' and pesquisa is not None:
        computadores = computadores.filter(
            Q(sistema_op__icontains=pesquisa) | Q(funcionario__nome__icontains=pesquisa) | Q(departamento__departamento__icontains=pesquisa) | Q(processador__modelo__icontains=pesquisa) | Q(id__iexact=pesquisa)
        )
    computadores = Paginator(computadores.order_by('id'), 5).get_page(pagina)
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
        'computador': Computador,
        'mensagens': []
    }
    if request.method == 'POST':
        form = ComputadorForm(request.POST)
        if form.is_valid():
            ip_data = ''
            mac_data = ''
            
            try:
                ip_data = VerificarIp(form.cleaned_data.get('endereco_ip'))
                try:
                    mac_data = VerificarMac(form.cleaned_data.get('endereco_mac'))
                    form.save()
                    pc_novo = Computador.objects.all().filter(gabinete__id=form.cleaned_data.get('gabinete').id).first()
                    computador_tipo = ContentType.objects.get(model='computador')

                    if ip_data is not None:
                        EnderecoIp(ip_address=ip_data,
                        content_type_id=computador_tipo.id, parent_object_id=pc_novo.id).save()
                    if mac_data is not None:
                        EnderecoMac(mac_address=mac_data,
                        content_type_id=computador_tipo.id, parent_object_id=pc_novo.id).save()

                    return redirect(computador_view, 1)

                except IndexError:
                    context['mensagens'].append('Esse endereço MAC já está em uso')
                    return render(request, template_name='computador/novo.html', context=context)

            except IndexError:
                context['mensagens'].append('Esse endereço IP já está em uso')
                return render(request, template_name='computador/novo.html', context=context)

        else:
                for valores in form.errors.values():
                    context['mensagens'].append(valores)
                
                context['field_erros'] = form.errors.keys()
    return render(request, template_name='computador/novo.html', context=context)


@login_required
@permission_required('dispositivo.change_computador', raise_exception=True)
def computador_edit(request, id):
    computador_db = get_object_or_404(Computador, pk=id)
    form = ComputadorForm(instance=computador_db)
    form_ip = EnderecoIp.objects.filter(computador=computador_db)
    form_mac = EnderecoMac.objects.filter(computador=computador_db)
    context = {
        'form': form,
        'computador': computador_db,
        'form_ip': form_ip,
        'form_mac': form_mac,
        'mensagens': []
    }
    if request.method == 'POST':
        form = ComputadorForm(request.POST, instance=computador_db)
        if form.is_valid():
            # Ok
            return redirect(computador_view, 1)
        else:
                for valores in form.errors.values():
                    context['mensagens'].append(valores)
                
                context['field_erros'] = form.errors.keys()       
    return render(request, template_name='computador/editar.html', context=context)


@login_required
@permission_required('dispositivo.view_roteador', raise_exception=True)
def roteador_view(request, pagina):
    pesquisa = request.GET.get('query')
    roteadores = Roteador.objects.all()
    if pesquisa != '' and pesquisa is not None:
        roteadores = roteadores.filter(
            Q(ssid__icontains=pesquisa) | Q(departamento__departamento__icontains=pesquisa) | Q(modelo__icontains=pesquisa)| Q(ip_roteador__ip_address__icontains=pesquisa)
            | Q(id__iexact=pesquisa) | Q(mac_roteador__mac_address__icontains=(pesquisa))
        )
    roteadores = Paginator(roteadores.order_by('id'), 5).get_page(pagina)
    content = {
        'roteadores': roteadores
    }
    return render(request, template_name='roteador/roteador.html', context=content)



