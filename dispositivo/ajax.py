from django.core.exceptions import ValidationError
from django.core.validators import validate_ipv4_address
from django.http.response import JsonResponse
from django.shortcuts import redirect, render
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

        elif tipo_data == 'selectPlacamae':
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
