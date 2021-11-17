from django.core.exceptions import ValidationError
from django.core.validators import validate_ipv4_address
from django.http.response import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required, permission_required
from .models import *
from dispositivo.models import *

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
@permission_required('dispositivo.view_impressora')
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

            html_item = f"""<tr class='mt-3' id="impressoraId{impressora.id}"><td><img style='width:60px;' class='rounded-circle me-2' src='' alt=""></td><td class='text-center'>{impressora.nome}</br>{impressora.modelo}</td><td>{impressora.departamento.predio}</td><td>{impressora.ip_impressora.first().ip_address}</td><td>GEST-103020</td><td><i onclick='VincularNovaImpressora({impressora.id})' class="fas fa-link"></i></td></tr>
            """
            data.append({
                'html_item': html_item,
                'nome': impressora.nome,
                'modelo': impressora.modelo,
                'ip': impressora.ip_impressora.first().ip_address
            })
        return JsonResponse(data={'impressoras': data}, safe=True)


@login_required
@permission_required('dispositivo.view_impressora')
def vincular_impressora_ajax(request):
    if request.method == 'GET':
        id_impressora = request.GET.get('id_impressora')
        id_computador = request.GET.get('id_computador')
        impressora = get_object_or_404(Impressora, pk=id_impressora)
        computador = get_object_or_404(Computador, pk=id_computador)
        pesquisa = Impressora.objects.filter(id=id_impressora, computador=computador)
        print(pesquisa)
        if pesquisa:
            computador.impressora.remove(impressora)
        else:
            computador.impressora.add(impressora)
    return JsonResponse(data={'sim': 'sim'}, safe=True)
