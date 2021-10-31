from django.core.paginator import Paginator
from django.http.response import JsonResponse
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required, permission_required
from django.forms import inlineformset_factory
from departamento.models import Funcionario
from .models import Computador, EnderecoIp, EnderecoMac, MemoriaRam
from .forms import ComputadorForm, EndereoIpForm, MemoriaRamForm
from django.contrib.contenttypes.models import ContentType
from django.db.models import Q, F


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
            outros_ips = EnderecoIp.objects.filter(ip_address=form.cleaned_data.get('endereco_ip'))
            outros_macs = EnderecoMac.objects.filter(mac_address=form.cleaned_data.get('endereco_mac'))

            if len(outros_ips) >= 1:
                context['mensagens'].append('Esse endereço IP já está em uso')
                return render(request, template_name='computador/novo.html', context=context)

            if len(outros_macs) >= 1:
                context['mensagens'].append('Esse endereço MAC já está em uso')
                return render(request, template_name='computador/novo.html', context=context)
            else:
                ip_data = form.cleaned_data.get('endereco_ip')
                mac_data = form.cleaned_data.get('endereco_mac')
                form.save()
                pc_novo = Computador.objects.all().filter(gabinete__id=form.cleaned_data.get('gabinete').id)
                computador_tipo = ContentType.objects.get(model='computador')
                for item in pc_novo:
                    EnderecoIp(ip_address=ip_data,
                    content_type_id=computador_tipo.id, parent_object_id=item.id).save()

                    EnderecoMac(mac_address=mac_data,
                    content_type_id=computador_tipo.id, parent_object_id=item.id).save()

                return redirect(computador_view, 1)
        else:
                for valores in form.errors.values():
                    context['mensagens'].append(valores)
                
                context['field_erros'] = form.errors.keys()
    return render(request, template_name='computador/novo.html', context=context)


