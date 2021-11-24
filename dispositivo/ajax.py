from django.core.exceptions import ValidationError
from django.core.validators import ip_address_validator_map, validate_ipv4_address
from django.http.response import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required, permission_required

from inventario.forms import ProcessadorForm
from .models import *
from dispositivo.models import *
from .forms import ComputadorForm, ComputadorFormInfo, ComputadorFormNovo, IpMacFormAtualizar
from netaddr import EUI


@login_required
@permission_required('dispositivo.add_computador', raise_exception=True)
def computador_create_ajax(request):
    if request.is_ajax():
        data = []
        lista_item = []
        tipo_data = request.GET.get('tipoValue')

        if tipo_data == 'selectFuncionario':
            lista_item = Funcionario.objects.all().order_by('nome')

        elif tipo_data == 'selectMouse':
            lista_item = Mouse.objects.all().filter(computador__isnull=True).order_by('criado_data')

        elif tipo_data == 'selectTeclado':
            lista_item = Teclado.objects.all().filter(computador__isnull=True).order_by('criado_data')

        elif tipo_data == 'selectMonitor':
            lista_item = Monitor.objects.all().filter(computador__isnull=True).order_by('criado_data')

        elif tipo_data == 'selectGabinete':
            lista_item = Gabinete.objects.all().filter(computador__isnull=True).order_by('criado_data')

        elif tipo_data == 'selectProcessador':
            lista_item = Processador.objects.all().filter(computador__isnull=True).order_by('criado_data')

        elif tipo_data == 'selectPlacamae' or tipo_data == 'selectPlaca_mae':
            lista_item = PlacaMae.objects.all().filter(computador__isnull=True).order_by('criado_data')

        elif tipo_data == 'selectHd':
            lista_item = Hd.objects.all().filter(computador__isnull=True).order_by('criado_data')

        for item in lista_item:
            data.append((f'{item.id}', str(item)))
        return JsonResponse(data, safe=False)

    return render(request, 'base.html')


@login_required
@permission_required('dispositivo.add_computador', raise_exception=True)
def verificar_ip_ajax(request):
    if request.is_ajax():
        ip = request.GET.get('enderecoip')
        data = {
            'ip': ip,
            'valido': False,
            'mensagem': ''
        }
        ip_db = EnderecoIp.objects.filter(ip_address=ip)
        if ip_db.count() >= 1:
            data['valido'] = False
            data['mensagem'] = 'Parece que algo já está usando esse endereço ip.'
        else:
            try:
                validador = validate_ipv4_address(ip)
                data['valido'] = True
            except ValidationError: 
                data['valido'] = False
                data['mensagem'] = 'Esse endereço não está no padrão IPV4.'
        return JsonResponse(data, safe=True)
    return render(request, 'base.html')

@login_required
@permission_required('dispositivo.view_impressora', raise_exception=True)
def impressora_pesquisa_ajax(request):
    if request.method == 'GET':
        impressoras = []
        data = []
        pesquisa = request.GET.get('query')
        id_computador = request.GET.get('id_computador')
        computador = get_object_or_404(Computador, pk=id_computador)
        if pesquisa:
            impressoras = Impressora.objects.filter(Q(nome__icontains=pesquisa) | Q(departamento__predio__icontains=pesquisa) | Q(ip_impressora__ip_address__icontains=pesquisa)).exclude(computador=computador)
        else:
            impressoras = Impressora.objects.exclude(computador=computador)

        for impressora in impressoras:
            predio = impressora.departamento.predio if impressora.departamento else 'Não selecionado'
            html_item = f"""<tr class='mt-3' id="impressoraId{impressora.id}"><td><img style='width:60px;' class='rounded-circle me-2' src='' alt=""></td><td class='text-center'>{impressora.nome}</br>{impressora.modelo}</td><td>{predio}</td><td>{impressora.ip_impressora.first().ip_address}</td><td>GEST-103020</td><td><i onclick='VincularNovaImpressora({impressora.id})' class="fas fa-link"></i></td></tr>
            """
            data.append({
                'html_item': html_item,
                'nome': impressora.nome,
                'modelo': impressora.modelo,
                'ip': impressora.ip_impressora.first().ip_address
            })
        return JsonResponse(data={'impressoras': data}, safe=True)


@login_required
@permission_required('dispositivo.view_impressora', raise_exception=True)
def vincular_impressora_ajax(request):
    if request.method == 'GET':
        id_impressora = request.GET.get('id_impressora')
        id_computador = request.GET.get('id_computador')
        impressora = get_object_or_404(Impressora, pk=id_impressora)
        computador = get_object_or_404(Computador, pk=id_computador)
        pesquisa = Impressora.objects.filter(id=id_impressora, computador=computador)
        if pesquisa:
            computador.impressora.remove(impressora)
        else:
            computador.impressora.add(impressora)
    return JsonResponse(data={'falha': 'sim'}, safe=True)


@login_required
@permission_required('dispositivo.change_computador', raise_exception=True)
def atualizar_computador_info_ajax(request):
    mensagens = []
    campo_erros = []
    if request.method == 'POST':
        id = request.POST.get("computador_id")
        computador = get_object_or_404(Computador, pk=id)
        form = ComputadorFormInfo(request.POST, instance=computador)
        if form.is_valid():
            # Validação Gabinete
            gabinete = Gabinete.objects.filter(computador=computador).first()
            if len(form.cleaned_data.get('gabinete')) >=1:
                gabinete.patrimonio = form.cleaned_data.get('gabinete')
                gabinete.save()
            else:
                Gabinete.objects.filter(computador=computador).update(patrimonio='')
            
            # validação HD
            if len(form.cleaned_data.get('hd')) >= 1:
                try: 
                    hd = Hd.objects.filter(computador=computador)
                    if hd.count() >= 1:
                        hd = hd.first()
                        hd.tamanho = form.cleaned_data.get('hd')
                        hd.save()
                    else:
                        novo_hd = Hd(modelo='Normal', tamanho_gb=int(form.cleaned_data.get('hd')))
                        novo_hd.tamanho = form.cleaned_data.get('hd')
                        novo_hd.save()
                        print(novo_hd)
                        computador.hd = novo_hd
                except ValueError:
                    campo_erros.append('id_hd')
                    mensagens.append('Tamanho do HD inválido, use um valor de 0 a 999')
                    return JsonResponse(status=404, data={'status':'false','messagem': mensagens, 'field_erros': campo_erros})

            
            # validação Monitor
            monitor1 = form.cleaned_data.get('monitor1')
            monitor2 = form.cleaned_data.get('monitor2')
            if len(monitor1) == 0 and len(monitor2) >=1:
                monitor1 = monitor2
                monitor2 = ''

            elif len(monitor1) >=1 and len(monitor2) >= 1:
                if monitor1 == monitor2:
                    monitor2 = ''

            if len(monitor1) >= 1:
                monitor = Monitor.objects.filter(computador=computador)
                if monitor.count() >= 1:
                    monitor = monitor.first()
                    monitor.patrimonio = monitor1
                    monitor.save()
                else:
                    novo_monitor = Monitor(marca='Não especificado', hdmi='Não', tamanho='0x0', patrimonio=monitor1)
                    novo_monitor.save()
                    computador.monitor.add(novo_monitor)
            else:
                monitor = Monitor.objects.filter(computador=computador)
                if monitor.count() >=1:
                    monitor = monitor.first()
                    if monitor.marca == 'Não especificado' and monitor.tamanho == '0x0':
                        computador.monitor.remove(monitor)
                        monitor.delete()
                    else:
                        computador.monitor.remove(monitor)

            if len(monitor2) >= 1:
                monitor = Monitor.objects.filter(computador=computador).exclude(patrimonio=monitor1)
                if monitor.count() >= 1:
                    monitor = monitor.first()
                    monitor.patrimonio = monitor2
                    monitor.save()
                else:
                    novo_monitor = Monitor(marca='Não especificado', hdmi='Não', tamanho='0x0', patrimonio=monitor2)
                    novo_monitor.save()
                    computador.monitor.add(novo_monitor)
            else:
                monitor = Monitor.objects.filter(computador=computador).exclude(patrimonio=monitor1)
                if monitor.count() >=1:
                    if monitor.first().marca == 'Não especificado' and monitor.first().tamanho == '0x0':
                        monitor = monitor.first()
                        computador.monitor.remove(monitor)
                        monitor.delete()
                    else:
                        computador.monitor.remove(monitor.first())

            form.save()
            return JsonResponse(status=200, safe=True, data={'data': 'data'})
        else:
            for valores in form.errors.values():
                mensagens.append(valores)
            for campo in form:
                if campo.errors:
                    campo_erros.append(campo.id_for_label)

    return JsonResponse(status=404, data={'status':'false','messagem': mensagens, 'field_erros': campo_erros})


@login_required
@permission_required('dispositivo.change_computador', raise_exception=True)
@permission_required('dispositivo.change_enderecoip', raise_exception=True)
def verificar_endereco_ip(request):
    mensagens = []
    campo_erros = []
    if request.method == 'POST':
        form = IpMacFormAtualizar(request.POST)
        if form.is_valid():
            id_computador = form.cleaned_data.get('parent_object_id')
            enderecoip = form.cleaned_data.get('ip_address')
            enderecomac = form.cleaned_data.get('endereco_mac')
            computador = get_object_or_404(Computador, pk=id_computador)
            
            if len(enderecoip) >=1:
                try:
                    if validate_ipv4_address(enderecoip) is None:
                        if EnderecoIp.objects.filter(ip_address=enderecoip).count() >=1:
                            endereco_bd = EnderecoIp.objects.filter(ip_address=enderecoip, computador=computador)
                            if endereco_bd.count() <= 0:
                                campo_erros.append('id_ip_address')
                                mensagens.append('Esse endereço de ip já está em uso.')
                                return JsonResponse(status=404, data={'status':'false','messagem': mensagens, 'field_erros': campo_erros})
                        else:
                            endereco_bd = EnderecoIp.objects.filter(computador=computador)
                            if endereco_bd.count() >=1:
                                endereco_bd = endereco_bd.first()
                                endereco_bd.ip_address = enderecoip
                                endereco_bd.save()
                            else:
                                novo_ip = EnderecoIp(ip_address=enderecoip, content_type_id= ContentType.objects.filter(model='computador').first().id, parent_object_id=computador.id)
                                novo_ip.save()
                                computador.ip_computador.add(novo_ip)
                except ValidationError:
                    campo_erros.append('id_ip_address')
                    mensagens.append('Isso não é um endereço ipv4')
                    return JsonResponse(status=404, data={'status':'false','messagem': mensagens, 'field_erros': campo_erros})
            else:
                endereco_bd = EnderecoIp.objects.filter(computador=computador)
                if endereco_bd.count() >=1:
                    endereco_bd = endereco_bd.first()
                    computador.ip_computador.remove(endereco_bd)
                    endereco_bd.delete()        

            consulta_computador_mac = EnderecoMac.objects.filter(computador=computador)

            if isinstance(enderecomac, EUI):
                # Consulta para ver se esse computador possui um mac já cadastrado.
                if consulta_computador_mac.count() >=1:
                    """Caso computador já possua um mac cadastrado."""
                    mac_antigo = consulta_computador_mac.first()
                    mac_antigo.mac_address = enderecomac
                    mac_antigo.save()
                else:
                    mac_novo = EnderecoMac(mac_address=enderecomac, content_type_id= ContentType.objects.filter(model='computador').first().id, parent_object_id=computador.id)
                    mac_novo.save()
            else:
                if consulta_computador_mac.count() >=1:
                    consulta_computador_mac.delete()

            return JsonResponse(status=200, safe=True, data={'data': 'data'})
        else:
            for valores in form.errors.values():
                mensagens.append(valores)
            for campo in form:
                if campo.errors:
                    campo_erros.append(campo.id_for_label)
    
    return JsonResponse(status=404, data={'status':'false','messagem': mensagens, 'field_erros': campo_erros})

@login_required
def atualizar_processador_ajax(request):
    mensagens = []
    campo_erros = []
    
    if request.method == 'POST':
        computador = get_object_or_404(Computador, pk=int(request.POST.get('id_computador')))
        form = None
        if computador.processador:
            processador = get_object_or_404(Processador, pk=computador.processador.id)
            form = ProcessadorForm(request.POST, instance=processador)
        else:
            form = ProcessadorForm(request.POST)

        if form.is_valid():
            processador_atualizado = form.save()
            if computador.processador:
                pass
            else:
                Computador.objects.filter(id=computador.id).update(processador=processador_atualizado)
                
            return JsonResponse(status=200, safe=True, data={'data': 'data'})
        else:
            for valores in form.errors.values():
                mensagens.append(valores)
            for campo in form:
                if campo.errors:
                    campo_erros.append(campo.id_for_label)
    
    return JsonResponse(status=404, data={'status':'false','messagem': mensagens, 'field_erros': campo_erros})

@login_required
@permission_required('dispositivo.add_computador', raise_exception=True)
def computador_novo_ajax(request):
    mensagens = []
    campo_erros = []
    if request.method == 'POST':
        usuario = request.POST.get('usuario')
        senha = request.POST.get('senha')
        valores = [request.POST]
        form = ComputadorFormNovo(request.POST)
        if form.is_valid():
            try:
                form.save()
                return JsonResponse(data={'data': 'data'}, safe=True)
            except ValueError as e:
                print(e)
                mensagens.append('Ocorreu um erro ao tentar salvar o computador. Tente Novamente.')
                for campo in form:
                    campo_erros.append(campo.id_for_label)

        else:
            for valores in form.errors.values():
                mensagens.append(valores)
            for campo in form:
                if campo.errors:
                    campo_erros.append(campo.id_for_label)
    
    if request.method == 'GET':
        departamentos = []
        for item in Departamento.objects.all():
            departamentos.append({
                'id': item.id,
                'nome': item.departamento,
            })
        data = {
            'departamentos': departamentos
        }
        return JsonResponse(status=200, data=data, safe=True)

    return JsonResponse(status=404, data={'status':'false','messagem': mensagens, 'field_erros': campo_erros})