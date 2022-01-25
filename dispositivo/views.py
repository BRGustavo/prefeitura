from functools import partialmethod
from django.core.checks.messages import Error
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
from .models import Computador, EnderecoIp, EnderecoIpReservado, EnderecoMac, Impressora, MemoriaRam, Roteador
from .forms import ComputadorForm, ComputadorFormDescricao, ComputadorFormInfo, ComputadorFormNovo, ComputadorFormRemover, EnderecoReservadoForm, IpMacFormAtualizar, RoteadorForm, ImpressoraForm
from inventario.forms import *
from django.contrib.contenttypes.models import ContentType
from django.db.models import Q, F
from utils import VerificarIp, VerificarMac
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from netaddr import EUI
from netaddr.core import AddrFormatError
from django.urls import reverse

@login_required
@permission_required('dispositivo.view_computador', raise_exception=True)
def computador_view(request, pagina):
    """
    Página responsável por listar os computadores do banco de dados no site.
    """
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
@permission_required('dispositivo.delete_computador', raise_exception=True)
def computador_remover(request):
    """
    Função chamada para remover um computador do banco de dados.
    Está como method GET, pois é convocado pelo ajax.
    """
    if request.method == 'GET':
        computador = get_object_or_404(Computador, pk=request.GET.get('id_computador'))
        for key,value in dict(request.GET).items():
            if key == 'manterGabinete':
                if value[0].lower() == 'sim':
                    if computador.gabinete and len(computador.gabinete.patrimonio):
                        computador.gabinete = None
                        computador.save()
                    else:
                        if computador.gabinete:
                            gabinete = computador.gabinete
                            computador.gabinete = None
                            computador.save()
                            gabinete.delete()
                else:
                    gabinete = computador.gabinete.id if computador.gabinete else None
                    if gabinete is not None:
                        computador.gabinete = None
                        computador.save()
                        Gabinete.objects.filter(id=gabinete).delete()
            if key == 'manterMonitor':
                monitores = Monitor.objects.filter(computador=computador)
                if monitores.count() >=1:
                    if value[0].lower() == 'sim':
                        for monitor in monitores:
                            if len(monitor.patrimonio) >=1:
                                computador.monitor.remove(monitor)
                                computador.save()
                            else:
                                computador.monitor.remove(monitor)
                                monitor.delete()
                    else:
                        for monitor in monitores:
                            computador.monitor.remove(monitor)
                            computador.save()
                            monitor.delete()

            if key == 'manterHd':
                hds = Hd.objects.filter(computador=computador)
                if hds.count() >=1:
                    if value[0].lower() == 'sim':
                        for hd in hds:
                            computador.hd = None
                            computador.save()
                    else:
                        for hd in hds:
                            computador.hd = None
                            computador.save()
                            hd.delete()
            if key == 'manterPlacaMae':
                placasMae = PlacaMae.objects.filter(computador=computador)
                if placasMae.count() >=1:
                    if value[0].lower() == 'sim':
                        for placa in placasMae:
                            computador.placa_mae = None
                            computador.save()
                    else:
                        for placa in placasMae:
                            computador.placa_mae = None
                            computador.save()
                            placa.delete()
                
            if key == 'manterProcessador':
                processadores = Processador.objects.filter(computador=computador)
                if processadores.count() >=1:
                    if value[0].lower() == 'sim':
                        for processador in processadores:
                            computador.processador = None
                            computador.save()
                    else:
                        for processador in processadores:
                            computador.processador = None
                            computador.save()
                            processador.delete()
        EnderecoIp.objects.filter(computador=computador).delete()
        EnderecoMac.objects.filter(computador=computador).delete()
        computador.delete()
        return JsonResponse(status=200, data={'data': 'apagado'}, safe=True)
        
    return JsonResponse(status=404, data={'messagem':['Erro teste']}, safe=True)

@login_required
@permission_required('dispositivo.view_computador', raise_exception=True)
def computador_visualizar(request, id, pagina='principal'):
    """
    Função responsável por retornar a página de cada computador individualmente utilizando como identificador o id fornecido pela url.
    """
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
        'formRemover': ComputadorFormRemover(),
    }
    if request.method == 'POST':
        form = ComputadorFormDescricao(request.POST, instance=computador)
        if form.is_valid():
            dados = form.save()
            return JsonResponse(status=200, data={'data':'data'}, safe=True)
        else:
            return JsonResponse(status=404, safe=True, data={'erro': 'erro'})
    if pagina == 'principal': # Função antigo sistema.
        return render(request, template_name='computador/visualizar.html', context=context)
    else:
        return render(request, template_name='computador/visualizar.html', context=context)


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
        departamento = roteador.departamento.id if roteador.departamento else ''
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
            
            endereco_ip = request.POST.get('endereco_ip')
            if endereco_ip is not None and len(endereco_ip) >=1:
                try:
                    if validate_ipv4_address(endereco_ip) is None:
                        consulta_db = EnderecoIp.objects.filter(ip_address=endereco_ip)
                        if consulta_db.count() >=1:
                            consulta_db = consulta_db.first()
                            if roteador_objeto_tipo == consulta_db.content_type_id and consulta_db.parent_object_id == roteador_db.id:
                                pass
                            else:
                                mensagens.append('Esse endereço IP já está em uso!')
                                campo_erros.append('id_endereco_ip')
                                return JsonResponse(status=404, data={'status':'false','messagem': mensagens, 'field_erros': campo_erros})
                        else:
                            consulta_ip_roteador = EnderecoIp.objects.filter(roteador=roteador_db)
                            if consulta_ip_roteador.count() >=1:
                                consulta_ip_roteador.update(ip_address=endereco_ip)
                            else: 
                                novo_ip = EnderecoIp(ip_address=endereco_ip, content_type_id=roteador_objeto_tipo, parent_object_id=roteador_db.id).save()
                                roteador_db.ip_roteador.add(novo_ip)

                except ValidationError:
                    mensagens.append('Endereço de IP informado não é um endereço IP válido!')
                    campo_erros.append('id_endereco_ip')
                    return JsonResponse(status=404, data={'status':'false','messagem': mensagens, 'field_erros': campo_erros})

            else:
                consulta_db = EnderecoIp.objects.filter(roteador=roteador_db)
                if consulta_db.count() >=1:
                    roteador_db.ip_roteador.remove(consulta_db.first())
                    consulta_db.delete()
                
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

@login_required
@permission_required('dispositivo.delete_roteador', raise_exception=True)
def roteador_delete(request):
    if request.method == 'GET':
        roteador_id = request.GET.get("roteador_id")
        roteador = get_object_or_404(Roteador, pk=roteador_id)
        if roteador:
            roteador.delete()
            return JsonResponse(status=200, data={'apagado':True, 'roteador_id':roteador_id}, safe=True)
        
    return JsonResponse(status=400, safe=True, data={'data':'data'})

def teste_view(request):
    pagina = 1
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
    return render(request, template_name='teste.html', context=content)


@login_required
def patrimonio_view(request):
    items = ''
    if request.method == 'GET':
        query = request.GET.get('query')
        if query is not None and len(query) >=1:
            gabinetes = Gabinete.objects.filter(Q(patrimonio__icontains=query))[0:20]
            monitores = Monitor.objects.filter(Q(patrimonio__icontains=query))[0:20]

            for gabinete in gabinetes:
                em_uso = 'Gabinete'
                departamento = 'Não Vinculado'
                try:                
                    link = reverse("computador_visualizar", args=[gabinete.computador.id, 'principal'])
                    em_uso = f'<a class="text-decoration-none text-dark" href="{link}"><b>Gabinete</b></a>' if gabinete.computador else 'Gabinete'
                except ObjectDoesNotExist:
                    em_uso = 'Gabinete'
                
                try:
                    departamento = gabinete.computador.departamento if gabinete.computador.departamento else 'Não vinculado'

                    if departamento == 'Não vinculado':
                        try:
                            departamento = gabinete.computador.funcionario.departamento.departamento if gabinete.computador.funcionario.departamento else 'Não vinculado'
                        except ObjectDoesNotExist:
                            departamento = 'Não vinculado'

                except ObjectDoesNotExist:
                    departamento = 'Não Vinculado'

                items += f"""
                    <div class="row p-1 ps-lg-3 m-0 mt-2 shadow d-flex" style="font-family: Arial, Helvetica, sans-serif;" id='modificar'>
                    <div class="col-auto p-0 d-flex align-items-center d-flex justify-content-center ">
                        <i class="fas fa-hdd fa-2x"></i>
                    </div>
                    <div class="col p-0 m-0 ps-3 d-flex justify-content-between">
                        <div class='item-esconder'>
                            <p class='mb-0 mt-2 '>{em_uso}</p>
                            <span class='d-flex d-flex flex-column flex-lg-row mt-1'>
                                <p class='mb-0 mt-0'>Patrimônio: {gabinete.patrimonio}</p>
                                <p class='mb-0 mt-0 ps-lg-2'>- {departamento}</p>
                            </span>
                        </div>
                    </div>
                </div>
                """


            for monitor in monitores:
                em_uso = 'Monitor'
                departamento = 'Não Vinculado'
                try:                
                    link = reverse("computador_visualizar", args=[monitor.computador.first().id, 'principal'])

                    em_uso = f'<a class="text-decoration-none text-dark" href="{link}"><b>Monitor</b></a>' if monitor.computador else 'Monitor'
                except ObjectDoesNotExist:
                    em_uso = 'Monitor'

                try:
                    pc_monitor = Computador.objects.filter(monitor=monitor).first()
                    departamento = pc_monitor.departamento.departamento if pc_monitor.departamento else 'Não vinculado'

                    if departamento == 'Não vinculado':
                        try:
                            departamento = pc_monitor.funcionario.departamento.departamento if pc_monitor.funcionario else 'Não vinculado'
                        except ObjectDoesNotExist:
                            departamento = 'Não vinculado'
                            
                except ObjectDoesNotExist:
                    departamento = 'Não Vinculado'

                items += f"""
                    <div class="row p-1 ps-lg-3 m-0 mt-2 shadow d-flex" style="font-family: Arial, Helvetica, sans-serif;" id='modificar'>
                    <div class="col-auto p-0 d-flex align-items-center d-flex justify-content-center ">
                        <i class="fas fa-hdd fa-2x"></i>
                    </div>
                    <div class="col p-0 m-0 ps-3 d-flex justify-content-between">
                        <div class='item-esconder'>
                            <p class='mb-0 mt-2 '><b>{em_uso}</b></p>
                            <span class='d-flex d-flex flex-column flex-lg-row mt-1'>
                                <p class='mb-0 mt-0'>Patrimônio: {monitor.patrimonio}</p>
                                <p class='mb-0 mt-0 ps-lg-2'>- {departamento}</p>
                            </span>
                        </div>
                    </div>
                </div>
                """
            return JsonResponse(status=200, data={'items': items}, safe=True)
    
    return render(request, template_name='patrimonios/patrimonio.html', context={'items':items})


def pesquisar_endereco_ip(request, pagina):
    pesquisa = request.GET.get('query')
    if request.method == 'GET':
        enderecos = EnderecoIp.objects.all()
        if pesquisa != '' and pesquisa is not None:
            enderecos = enderecos.filter(Q(ip_address__icontains=pesquisa))
    
        items = []
        # enderecos = Paginator(enderecos.order_by('ip_address'), 15).get_page(pagina)
        for endereco in enderecos:
            tipo = 'Computador'
            if isinstance(endereco.parent_object, Impressora):
                tipo = 'Impressora'
            elif isinstance(endereco.parent_object, Computador):
                tipo = 'Computador'
            elif isinstance(endereco.parent_object, Roteador):
                tipo = 'Roteador'
            elif isinstance(endereco.parent_object, EnderecoIpReservado):
                tipo = 'Reservado'
            else:
                tipo = 'Desconhecido'
            items.append({
                'id': endereco.parent_object.id,
                'tipo': tipo,
                'ip': endereco.ip_address,
                'parente': endereco.parent_object,
            })
        items = Paginator(items, 15).get_page(pagina)
    return render(request, template_name='consulta_ip.html', context={'enderecos': items,  'form': EnderecoReservadoForm()})

# def pesquisar_endereco_ip(request):
#     if request.method == 'GET':
#         enderecos = EnderecoIp.objects.all()
#         data = []
#         query = request.GET.get('query')
#         rede4 = request.GET.get('rede4') 
#         rede5 = request.GET.get('rede5') 
#         rede15 = request.GET.get('rede15')
#         reservado = request.GET.get('reservado')
#         retornar_json = False

#         if query is not None and len(query) >=1:
#             enderecos = EnderecoIp.objects.filter(Q(ip_address__icontains=query))
        
#         if rede4 == 'false' and rede5=='false' and rede15 == 'false' and reservado == 'false':
#             rede4, rede5, rede15, reservado = ('true', 'true', 'true', 'true')
        
#         for item in enderecos:

#             nome_dispositivo = 'Não Identificado'
#             modelo = ContentType.objects.filter(id=item.content_type_id).first().model
#             mac = EnderecoMac.objects.filter(parent_object_id=item.parent_object_id, content_type_id=item.content_type_id).first()
#             if mac is None:
#                 mac = '-'
#             else:
#                 mac = mac.endereco_mac
            
#             if str(modelo) == 'computador':
#                 nome_dispositivo = 'Computador'
#                 nome_dispositivo = f"""
#                 <a class='text-decoration-none' href='{reverse("computador_visualizar", args=[item.parent_object_id, 'principal'])}'>Computador</a>"""
#             elif str(modelo) == 'impressora':
#                 nome_dispositivo = 'Impressora'
#             elif str(modelo) == 'roteador':
#                 nome_dispositivo = 'Roteador'
#             elif str(modelo) == 'enderecoipreservado':
#                 nome_dispositivo = 'Reservado'

#             teste_logico = nome_dispositivo == 'Reservado' and reservado == 'false'
#             if ('192.168.4' in str(item.ip_address) and rede4 == 'false'):
#                 if nome_dispositivo == 'Reservado':
#                     if teste_logico:
#                         continue
#                 else:
#                     continue
#             elif '192.168.5' in str(item.ip_address) and rede5 == 'false':
#                 if nome_dispositivo == 'Reservado':
#                     if teste_logico:
#                         continue
#                 else:
#                     continue
#             elif '192.168.15' in str(item.ip_address) and rede15 == 'false':
#                 if nome_dispositivo == 'Reservado':
#                     if teste_logico:
#                         continue
#                 else:
#                     continue
#             elif teste_logico:
#                 continue
            
            
#             if nome_dispositivo != 'Reservado':
#                 data.append(f"""
#                     <li class="list-group-item" style="font-family: Arial, Helvetica, sans-serif;">
#                         <div class="row d-flex align-items-center">
#                             <div class="col-auto">
#                                 <i class="fas fa-network-wired text-success"></i>
#                             </div>
#                             <div class="col-auto">
#                                 <p class='text mb-0 pb-0'><b>{nome_dispositivo} - {item.ip_address}</b></p>
#                                 <p class='mb-0 text-dark'>Endereço MAC: {mac} </p>
#                             </div>
#                         </div>
#                     </li>
#                     """
#                 )
#             else:
#                 objeto_reservado = EnderecoIpReservado.objects.filter(id=item.parent_object_id).first()
#                 titulo = objeto_reservado.titulo if objeto_reservado.titulo else 'Reservado'
#                 data.append(f"""
#                     <li class="list-group-item" style="font-family: Arial, Helvetica, sans-serif;">
#                         <div class="row d-flex align-items-center text-black">
#                             <div class="col-auto">
#                                 <i class="fas fa-network-wired text-danger"></i>
#                             </div>
#                             <div class="col-auto">
#                                 <p class=' mb-0 pb-0'><b>{titulo} - {item.ip_address}</b></p>
#                                 <p class='mb-0'>Endereço MAC não disponível </p>
#                             </div>
#                             <div class="col d-flex flex-row-reverse d-flex align-items-center">
#                                 <i onclick="RemoverIPReservado('{objeto_reservado.id}')" class="far fa-trash-alt text-danger"></i>
#                             </div>
#                         </div>
#                     </li>
#                     """
#                 )
#         if (query is not None and len(query) >=1) or request.is_ajax():
#             return JsonResponse(status=200, data={'enderecos': data}, safe=True)

#     return render(request, template_name='consulta_ip.html', context={'enderecos': data, 'form': EnderecoReservadoForm()})