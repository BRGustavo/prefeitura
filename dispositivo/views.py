from django.core.paginator import Paginator
from django.http.response import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required, permission_required
from django.core.validators import validate_ipv4_address
from django.forms import inlineformset_factory
from macaddress import format_mac, mac_linux
import netaddr
from netaddr.strategy.eui48 import mac_bare
from departamento.forms import FuncionarioForm
from departamento.models import Departamento, Funcionario
from .models import Computador, EnderecoIp, EnderecoMac, Impressora, MemoriaRam, Roteador
from .forms import ComputadorForm, ComputadorFormDescricao, ComputadorFormInfo, ComputadorFormNovo, IpMacFormAtualizar, RoteadorForm, ImpressoraForm
from inventario.forms import *
from django.contrib.contenttypes.models import ContentType
from django.db.models import Q, F
from utils import VerificarIp, VerificarMac
from django.core.exceptions import ValidationError
from netaddr import EUI
from netaddr.core import AddrFormatError


@login_required
@permission_required('dispositivo.view_computador', raise_exception=True)
def computador_view(request, pagina):
    pesquisa = request.GET.get('query')
    computadores = Computador.objects.all()
    if pesquisa != '' and pesquisa is not None:
        computadores = computadores.filter(
            Q(nome_rede__icontains=pesquisa) | Q(sistema_op__icontains=pesquisa) | Q(funcionario__nome__icontains=pesquisa) | Q(departamento__departamento__icontains=pesquisa) | Q(processador__modelo__icontains=pesquisa) | Q(departamento__singla_departamento__icontains=pesquisa) | Q(ip_computador__ip_address__icontains=pesquisa) | Q(mac_computador__mac_address__icontains=pesquisa)| Q(id__iexact=pesquisa)
        )
    computadores = Paginator(computadores.order_by('id'), 15).get_page(pagina)
    content = {
        'computadores': computadores,
        'formComputador': ComputadorFormNovo()
    }
    return render(request, template_name='computador/computador.html', context=content)


@login_required
@permission_required('dispositivo.add_computador', raise_exception=True)
def computador_create(request):
    form = ComputadorForm()
    context = {
        'form': form,
        'formFuncionario': FuncionarioForm(),
        'formTeclado': TecladoForm(),
        'formMouse': MouseForm(),
        'formGabinete': GabineteForm(),
        'formPlacaMae': PlacaMaeForm(),
        'formProcessador': ProcessadorForm(),
        'formHd': HdForm(),
        'formMonitor': MonitorForm(),
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
        computador_objeto_tipo = ContentType.objects.filter(model='computador').first().id
        if form.is_valid():
            endereco_ip_formulario = form.cleaned_data['endereco_ip']
            endereco_mac_formulario = form.cleaned_data['endereco_mac']

            if len(endereco_ip_formulario) >= 1:
                # Consulta para ver se esse computador possui um ip já cadastrado.
                consulta_computador_ip = EnderecoIp.objects.filter(computador=computador_db)

                if consulta_computador_ip.count() >= 1:
                    """Caso exista um ip cadastrado para esse computador na tabela de ips."""
                    try: 
                        if validate_ipv4_address(endereco_ip_formulario) is None:
                            # Consulta para verificar se há um ip já cadastrado igual ao ip do formulário.
                            endereco_ip_db = EnderecoIp.objects.filter(ip_address=endereco_ip_formulario)
                            if endereco_ip_db.count() >= 1:
                                if endereco_ip_db.first().parent_object_id != computador_db.id:
                                    """Caso esse ip já exista e seja de outro dono, vai mostrar uma msg no front."""
                                    context['mensagens'].append('Você está tentando usar um ip já utilizado por outro dispositivo.')
                                    return render(request, template_name='computador/editar.html', context=context)
                            else:
                                """Atualizando o ip antigo já vinculado ao outro computador"""
                                ip_velho = consulta_computador_ip.first()
                                ip_velho.ip_address = endereco_ip_formulario
                                ip_velho.save()

                    except ValidationError:
                        """Endereço de ip informado não é valido."""
                        context['mensagens'].append('Valor digitado não é um ip ou não é um ipv4 válido.')
                        return render(request, template_name='computador/editar.html', context=context)

                else:
                    """Computador ainda não possui um ip cadastrado."""
                    try: 
                        if validate_ipv4_address(endereco_ip_formulario) is None:
                            # Consultando o ip no banco de dados.
                            ip_base_dados = EnderecoIp.objects.filter(ip_address=endereco_ip_formulario)
                            if ip_base_dados.count() >= 1:
                                """IP já possui outro dispositivo dono, portanto não pode ser inserido."""
                                context['mensagens'].append('Você está tentando usar um ip já utilizado por outro dispositivo.')
                                return render(request, template_name='computador/editar.html', context=context)
                            else:

                                novo_ip = EnderecoIp(ip_address=endereco_ip_formulario, content_type_id= computador_objeto_tipo, parent_object_id=computador_db.id)
                                novo_ip.save()

                    except ValidationError:
                        """Endereço de ip informado não é valido."""
                        context['mensagens'].append('Valor digitado não é um ip ou não é um ipv4 válido.')
                        return render(request, template_name='computador/editar.html', context=context)
            else:
                """Caso o usuário não tenha informado nada no campo ip."""
                consulta_computador_ip = EnderecoIp.objects.filter(computador=computador_db)
                if consulta_computador_ip.count() >= 1:
                    ip_antigo = consulta_computador_ip.first()
                    ip_antigo.delete()

            
            consulta_computador_mac = EnderecoMac.objects.filter(computador=computador_db)

            if isinstance(endereco_mac_formulario, EUI):
                # Consulta para ver se esse computador possui um mac já cadastrado.
                if consulta_computador_mac.count() >=1:
                    """Caso computador já possua um mac cadastrado."""
                    mac_antigo = consulta_computador_mac.first()
                    mac_antigo.mac_address = endereco_mac_formulario
                    mac_antigo.save()
                else:
                    mac_novo = EnderecoMac(mac_address=endereco_mac_formulario, content_type_id= computador_objeto_tipo, parent_object_id=computador_db.id)
                    mac_novo.save()
            else:
                if consulta_computador_mac.count() >=1:
                    consulta_computador_mac.delete()

            form.save()
            return redirect(computador_visualizar, computador_db.id, 'principal')
        else:
                for valores in form.errors.values():
                    context['mensagens'].append(valores)
                
                context['field_erros'] = form.errors.keys()       
    return render(request, template_name='computador/editar.html', context=context)

@login_required
@permission_required('dispositivo.view_computador', raise_exception=True)
def computador_visualizar(request, id, pagina='principal'):
    computador = get_object_or_404(Computador, pk=id)
    form = ComputadorForm(instance=computador)
    formInfo = ComputadorFormInfo(instance=computador)

    formIpMac = IpMacFormAtualizar(initial={
        'object_id': ContentType.objects.filter(model='computador').first().id,
        'parent_object_id': computador.id,
        'ip_address':computador.ip_computador.first().ip_address if computador.ip_computador.count() >=1 else '',
        'endereco_mac':computador.mac_computador.first().mac_address if computador.mac_computador.count() >=1 else ''
        })

    formProcessador = ProcessadorForm()
    processador_pc = Processador.objects.all().filter(computador=computador)
    if processador_pc.count() >=1:
        processador_id = get_object_or_404(Processador, pk=processador_pc.first().id) 
        formProcessador = ProcessadorForm(instance=processador_id)

    formPlacaMae = PlacaMaeForm()
    placamae_pc = PlacaMae.objects.all().filter(computador=computador)
    if placamae_pc.count() >=1:
        placamae_id = get_object_or_404(PlacaMae, pk=placamae_pc.first().id) 
        formPlacaMae = PlacaMaeForm(instance=placamae_id)

    context = {
        'computador': computador,
        'formComputador': form,
        'formInfo': formInfo,
        'formIpMac': formIpMac,
        'formProcessador': formProcessador,
        'formPlacaMae': formPlacaMae,
        'funcionarios': Funcionario.objects.all(),
        
    }
    if request.method == 'POST':
        form = ComputadorFormDescricao(request.POST, instance=computador)
        if form.is_valid():
            dados = form.save()
            return JsonResponse(status=200, data={'data':'data'}, safe=True)
        else:
            return JsonResponse(status=404, safe=True, data={'erro': 'erro'})
    if pagina == 'principal':
        return render(request, template_name='computador/visualizar.html', context=context)
    elif pagina == 'rede':
        return render(request, template_name='computador/visualizar_rede.html', context=context)
    elif pagina == 'processador':
        return render(request, template_name="computador/visualizar_processador.html", context=context)
    elif pagina == 'placa_mae':
        return render(request, template_name='computador/visualizar_placa_mae.html', context=context)


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
    roteadores = Paginator(roteadores.order_by('id'), 10).get_page(pagina)
    content = {
        'roteadores': roteadores,
        'form': RoteadorForm(),
    }
    return render(request, template_name='roteador/roteador.html', context=content)


@login_required
@permission_required('dispositivo.add_roteador')
def roteador_add(request):
    campo_erros = []
    mensagens = []

    if request.method == 'POST':
        form = RoteadorForm(request.POST)
        if form.is_valid():
            ip_data = ''
            try:
                ip_data = VerificarIp(form.cleaned_data.get('endereco_ip'))
                try:
                    if isinstance(form.cleaned_data.get('endereco_mac'), EUI):
                        mac_data = VerificarMac(form.cleaned_data.get('endereco_mac'))
                    else:
                        mac_data = None
                    roteador_novo = form.save()
                    roteador_tipo = ContentType.objects.get(model='roteador')

                    if ip_data is not None:
                        EnderecoIp(ip_address=ip_data,
                        content_type_id=roteador_tipo.id, parent_object_id=roteador_novo.id).save()
                    if mac_data is not None:
                        print(mac_data)
                        EnderecoMac(mac_address=mac_data,
                        content_type_id=roteador_tipo.id, parent_object_id=roteador_novo.id).save()

                    return JsonResponse(status=200, data={'data':'data'}, safe=True)

                except IndexError:
                    mensagens.append('Esse endereço MAC já está em uso')
                    campo_erros.append('endereco_mac')

            except IndexError:
                mensagens.append('Esse endereço IP já está em uso')
                campo_erros.append('endereco_ip')
        else:
            for valores in form.errors.values():
                mensagens.append(valores)
                for campo in form:
                    if campo.errors:
                        campo_erros.append(campo.id_for_label)

    return JsonResponse(status=404, data={'status':'false','messagem': mensagens, 'field_erros': campo_erros})


@login_required
@permission_required('dispositivo.change_roteador', raise_exception=True)
def roteador_edit(request):
    id = 0
    campo_erros = []
    mensagens = []

    if request.method == 'GET':
        id = request.GET.get('roteador_id')
        roteador = Roteador.objects.filter(id=id).first()
        ip = ''
        mac = ''
        departamento = roteador.departamento.id if roteador.departamento else None
        if roteador.ip_roteador.count():
            ip = roteador.ip_roteador.first().ip_address
        if roteador.mac_roteador.count():
            mac = roteador.mac_roteador.first().mac_address

        data = {
            'campos':
                {
                    'roteador_id': roteador.id,
                    'ssid': roteador.ssid,
                    'senha': roteador.senha,
                    'modelo': roteador.modelo,
                    'endereco_ip': ip,
                    'endereco_mac': mac,
                    'departamento': departamento,
                    'descricao': roteador.descricao,
                }
        }
        return JsonResponse(status=200, data=data, safe=True)

    if request.method == 'POST':
        roteador_db = get_object_or_404(Roteador, pk=request.POST.get('roteador_id'))
        form = RoteadorForm(request.POST, instance=roteador_db)
        roteador_objeto_tipo = ContentType.objects.filter(model='roteador').first().id
        if form.is_valid():
            
            form.save()
            return JsonResponse(status=200, data={'data': 'data'}, safe=True)
        else:
            for valores in form.errors.values():
                mensagens.append(valores)
                for campo in form:
                    if campo.errors:
                        campo_erros.append(campo.id_for_label)

    return JsonResponse(status=404, data={'status':'false','messagem': mensagens, 'field_erros': campo_erros})


@login_required
@permission_required('dispositivo.view_impressora', raise_exception=True)
def impressora_view(request, pagina):
    pesquisa = request.GET.get('query')
    impressoras = Impressora.objects.all()
    if pesquisa != '' and pesquisa is not None:
        impressoras = impressoras.filter(
            Q(matricula__icontains=pesquisa) | Q(nome__icontains=pesquisa) | Q(ip_impressora__ip_address__icontains=pesquisa) | Q(mac_impressora__mac_address__icontains=pesquisa) | Q(departamento__departamento__icontains=pesquisa) | Q(departamento__singla_departamento__icontains=pesquisa)| Q(local__icontains=pesquisa) | Q(id__iexact=pesquisa))

    impressoras = Paginator(impressoras.order_by('id'), 10).get_page(pagina)
    content = {
        'impressoras': impressoras,
        'form': ImpressoraForm()
    }
    return render(request, template_name='impressora/impressora.html', context=content)

@login_required
@permission_required('dispositivo.delete_impressora', raise_exception=True)
def impressora_delete(request):
    if request.method == 'GET':
        impressora_id = request.GET.get("impressora_id")
        impressora = get_object_or_404(Impressora, pk=impressora_id)
        if impressora:
            impressora.delete()
            return JsonResponse(status=200, data={'apagado':True, 'impressora_id':impressora_id}, safe=True)
        
    return JsonResponse(status=400, safe=True, data={'data':'data'})


def teste_view(request):
    pagina = 1
    """Função responsável pelo template de listar os usuários """
    pesquisa = request.GET.get('query')
    formFuncionario = FuncionarioForm()
    funcionarios_lista = Funcionario.objects.all()
    if pesquisa != '' and pesquisa is not None:

        funcionarios_lista = funcionarios_lista.filter(
            Q(nome__icontains=pesquisa) | Q(sobrenome__icontains=pesquisa) | Q(departamento__departamento__icontains=pesquisa) | Q(departamento__predio__icontains=pesquisa) | Q(controle_acesso__icontains=pesquisa) | Q(id__iexact=pesquisa) | Q(usuario_pc__icontains=pesquisa)
        )

    funcionarios = Paginator(funcionarios_lista.order_by('id'), 10).get_page(pagina)

    content = {
        'funcionarios': funcionarios,
        'pesquisa':pesquisa,
        'formFuncionario': formFuncionario,

    }
    return render(request, template_name='teste.html', context=content)