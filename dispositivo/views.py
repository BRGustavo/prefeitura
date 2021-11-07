from django.core.paginator import Paginator
from django.http.response import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required, permission_required
from django.core.validators import validate_ipv4_address
from django.forms import inlineformset_factory
from departamento.forms import FuncionarioForm
from .models import Computador, EnderecoIp, EnderecoMac, Impressora, MemoriaRam, Roteador
from .forms import ComputadorForm, RoteadorForm, ImpressoraForm
from inventario.forms import *
from django.contrib.contenttypes.models import ContentType
from django.db.models import Q, F
from utils import VerificarIp, VerificarMac
from django.core.exceptions import ValidationError
from netaddr import EUI


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


@login_required
@permission_required('dispositivo.add_roteador')
def roteador_add(request):
    form = RoteadorForm()
    context = {
        'form': form,
        'mensagens': []
    }
    if request.method == 'POST':
        form = RoteadorForm(request.POST)
        if form.is_valid():
            ip_data = ''
            
            try:
                ip_data = VerificarIp(form.cleaned_data.get('endereco_ip'))
                try:
                    if isinstance(form.cleaned_data.get('endereco_mac'), EUI):
                        mac_data = VerificarMac(form.cleaned_data.get('endereco_mac'))

                    roteador_novo = form.save()
                    roteador_tipo = ContentType.objects.get(model='roteador')

                    if ip_data is not None:
                        EnderecoIp(ip_address=ip_data,
                        content_type_id=roteador_tipo.id, parent_object_id=roteador_novo.id).save()
                    if mac_data is not None:
                        print(mac_data)
                        EnderecoMac(mac_address=mac_data,
                        content_type_id=roteador_tipo.id, parent_object_id=roteador_novo.id).save()

                    return redirect(roteador_view, 1)

                except IndexError:
                    context['mensagens'].append('Esse endereço MAC já está em uso')
                    return render(request, template_name='roteador/novo.html', context=context)

            except IndexError:
                context['mensagens'].append('Esse endereço IP já está em uso')
                return render(request, template_name='roteador/novo.html', context=context)

        else:
                for valores in form.errors.values():
                    context['mensagens'].append(valores)
                
                context['field_erros'] = form.errors.keys()
    return render(request, template_name='roteador/novo.html', context=context)


@login_required
@permission_required('dispositivo.change_roteador', raise_exception=True)
def roteador_edit(request, id):
    roteador_db = get_object_or_404(Roteador, pk=id)
    form = RoteadorForm(instance=roteador_db)
    form_ip = EnderecoIp.objects.filter(roteador=roteador_db)
    form_mac = EnderecoMac.objects.filter(roteador=roteador_db)
    context = {
        'form': form,
        'roteador': roteador_db,
        'form_ip': form_ip,
        'form_mac': form_mac,
        'mensagens': []
    }
    if request.method == 'POST':
        form = RoteadorForm(request.POST, instance=roteador_db)
        roteador_objeto_tipo = ContentType.objects.filter(model='roteador').first().id
        if form.is_valid():
            endereco_ip_formulario = form.cleaned_data['endereco_ip']
            endereco_mac_formulario = form.cleaned_data['endereco_mac']

            if len(endereco_ip_formulario) >= 1:
            # Consulta para ver se esse roteador possui um ip já cadastrado.
                consulta_roteador_ip = EnderecoIp.objects.filter(roteador=roteador_db)

                if consulta_roteador_ip.count() >= 1:
                    """Caso exista um ip cadastrado para esse roteador na tabela de ips."""
                    try: 
                        if validate_ipv4_address(endereco_ip_formulario) is None:
                            # Consulta para verificar se há um ip já cadastrado igual ao ip do formulário.
                            endereco_ip_db = EnderecoIp.objects.filter(ip_address=endereco_ip_formulario)
                            if endereco_ip_db.count() >= 1:
                                if endereco_ip_db.first().parent_object_id != roteador_db.id:
                                    """Caso esse ip já exista e seja de outro dono, vai mostrar uma msg no front."""
                                    context['mensagens'].append('Você está tentando usar um ip já utilizado por outro dispositivo.')
                                    return render(request, template_name='roteador/editar.html', context=context)
                            else:
                                """Atualizando o ip antigo já vinculado ao outro roteador"""
                                ip_velho = consulta_roteador_ip.first()
                                ip_velho.ip_address = endereco_ip_formulario
                                ip_velho.save()

                    except ValidationError:
                        """Endereço de ip informado não é valido."""
                        context['mensagens'].append('Valor digitado não é um ip ou não é um ipv4 válido.')
                        return render(request, template_name='roteador/editar.html', context=context)

                else:
                        """Roteador ainda não possui um ip cadastrado."""
                        try: 
                            if validate_ipv4_address(endereco_ip_formulario) is None:
                                # Consultando o ip no banco de dados.
                                ip_base_dados = EnderecoIp.objects.filter(ip_address=endereco_ip_formulario)
                                if ip_base_dados.count() >= 1:
                                    """IP já possui outro dispositivo dono, portanto não pode ser inserido."""
                                    context['mensagens'].append('Você está tentando usar um ip já utilizado por outro dispositivo.')
                                    return render(request, template_name='roteador/editar.html', context=context)
                                else:

                                    novo_ip = EnderecoIp(ip_address=endereco_ip_formulario, content_type_id= roteador_objeto_tipo, parent_object_id=roteador_db.id)
                                    novo_ip.save()

                        except ValidationError:
                            """Endereço de ip informado não é valido."""
                            context['mensagens'].append('Valor digitado não é um ip ou não é um ipv4 válido.')
                            return render(request, template_name='roteador/editar.html', context=context)
            else:
                """Caso o usuário não tenha informado nada no campo ip."""
                consulta_roteador_ip = EnderecoIp.objects.filter(roteador=roteador_db)
                if consulta_roteador_ip.count() >= 1:
                    ip_antigo = consulta_roteador_ip.first()
                    ip_antigo.delete()

            # Consulta para ver se esse roteador possui um mac já cadastrado.
            consulta_roteador_mac = EnderecoMac.objects.filter(roteador=roteador_db)
            if isinstance(endereco_mac_formulario, EUI):
                if consulta_roteador_mac.count() >=1:
                    """Caso roteador já possua um mac cadastrado."""
                    mac_antigo = consulta_roteador_mac.first()
                    mac_antigo.mac_address = endereco_mac_formulario
                    mac_antigo.save()
                else:
                    mac_novo = EnderecoMac(mac_address=endereco_mac_formulario, content_type_id= roteador_objeto_tipo, parent_object_id=roteador_db.id)
                    mac_novo.save()

            else:
                if consulta_roteador_mac.count() >=1:
                    consulta_roteador_mac.delete()

            form.save()
            return redirect(roteador_view, 1)
        else:
                for valores in form.errors.values():
                    context['mensagens'].append(valores)
                
                context['field_erros'] = form.errors.keys()       
    return render(request, template_name='roteador/editar.html', context=context)


@login_required
@permission_required('dispositivo.view_impressora', raise_exception=True)
def impressora_view(request, pagina):
    pesquisa = request.GET.get('query')
    impressoras = Impressora.objects.all()
    if pesquisa != '' and pesquisa is not None:
        impressoras = impressoras.filter(
            Q(patrimonio__icontains=pesquisa) | Q(nome__icontains=pesquisa) | Q(ip_impressora__ip_address__icontains=pesquisa) | Q(departamento__departamento__icontains=pesquisa) | Q(local__icontains=pesquisa) | Q(id__iexact=pesquisa))

    impressoras = Paginator(impressoras.order_by('id'), 5).get_page(pagina)
    content = {
        'impressoras': impressoras
    }
    return render(request, template_name='impressora/impressora.html', context=content)


@login_required
@permission_required('dispositivo.add_impressora', raise_exception=True)
def impressora_add(request):
    form = ImpressoraForm()
    context = {
        'form': form,
        'mensagens': []
    }
    if request.method == 'POST':
        form = ImpressoraForm(request.POST)
        if form.is_valid():
            ip_data = ''
            mac_data = ''
            
            try:
                ip_data = VerificarIp(form.cleaned_data.get('endereco_ip'))
                try:
                    mac_data = VerificarMac(form.cleaned_data.get('endereco_mac'))
                    pc_novo = form.save()
                    impressora_tipo = ContentType.objects.get(model='impressora')

                    if ip_data is not None:
                        EnderecoIp(ip_address=ip_data,
                        content_type_id=impressora_tipo.id, parent_object_id=pc_novo.id).save()
                    if mac_data is not None:
                        EnderecoMac(mac_address=mac_data,
                        content_type_id=impressora_tipo.id, parent_object_id=pc_novo.id).save()

                    return redirect(impressora_view, 1)

                except IndexError:
                    context['mensagens'].append('Esse endereço MAC já está em uso')
                    return render(request, template_name='impressora/novo.html', context=context)

            except IndexError:
                context['mensagens'].append('Esse endereço IP já está em uso')
                return render(request, template_name='impressora/novo.html', context=context)

        else:
                for valores in form.errors.values():
                    context['mensagens'].append(valores)
                
                context['field_erros'] = form.errors.keys()
    return render(request, template_name='impressora/novo.html', context=context)

@login_required
@permission_required('dispositivo.change_impressora', raise_exception=True)
def impressora_edit(request, id):
    impressora_db = get_object_or_404(Impressora, pk=id)
    form = ImpressoraForm(instance=impressora_db)
    form_ip = EnderecoIp.objects.filter(impressora=impressora_db)
    form_mac = EnderecoMac.objects.filter(impressora=impressora_db)
    context = {
        'form': form,
        'impressora': impressora_db,
        'form_ip': form_ip,
        'form_mac': form_mac,
        'mensagens': []
    }
    if request.method == 'POST':
        form = ImpressoraForm(request.POST, instance=impressora_db)
        impressora_objeto_tipo = ContentType.objects.filter(model='impressora').first().id
        if form.is_valid():
            endereco_ip_formulario = form.cleaned_data['endereco_ip']
            endereco_mac_formulario = form.cleaned_data['endereco_mac']

            if len(endereco_ip_formulario) >= 1:
                # Consulta para ver se esse impressora possui um ip já cadastrado.
                consulta_impressora_ip = EnderecoIp.objects.filter(impressora=impressora_db)

                if consulta_impressora_ip.count() >= 1:
                    """Caso exista um ip cadastrado para esse impressora na tabela de ips."""
                    try: 
                        if validate_ipv4_address(endereco_ip_formulario) is None:
                            # Consulta para verificar se há um ip já cadastrado igual ao ip do formulário.
                            endereco_ip_db = EnderecoIp.objects.filter(ip_address=endereco_ip_formulario)
                            if endereco_ip_db.count() >= 1:
                                if endereco_ip_db.first().parent_object_id != impressora_db.id:
                                    """Caso esse ip já exista e seja de outro dono, vai mostrar uma msg no front."""
                                    context['mensagens'].append('Você está tentando usar um ip já utilizado por outro dispositivo.')
                                    return render(request, template_name='impressora/editar.html', context=context)
                            else:
                                """Atualizando o ip antigo já vinculado ao outro impressora"""
                                ip_velho = consulta_impressora_ip.first()
                                ip_velho.ip_address = endereco_ip_formulario
                                ip_velho.save()

                    except ValidationError:
                        """Endereço de ip informado não é valido."""
                        context['mensagens'].append('Valor digitado não é um ip ou não é um ipv4 válido.')
                        return render(request, template_name='impressora/editar.html', context=context)

                else:
                    """Impressora ainda não possui um ip cadastrado."""
                    try: 
                        if validate_ipv4_address(endereco_ip_formulario) is None:
                            # Consultando o ip no banco de dados.
                            ip_base_dados = EnderecoIp.objects.filter(ip_address=endereco_ip_formulario)
                            if ip_base_dados.count() >= 1:
                                """IP já possui outro dispositivo dono, portanto não pode ser inserido."""
                                context['mensagens'].append('Você está tentando usar um ip já utilizado por outro dispositivo.')
                                return render(request, template_name='impressora/editar.html', context=context)
                            else:

                                novo_ip = EnderecoIp(ip_address=endereco_ip_formulario, content_type_id=impressora_objeto_tipo, parent_object_id=impressora_db.id)
                                novo_ip.save()

                    except ValidationError:
                        """Endereço de ip informado não é valido."""
                        context['mensagens'].append('Valor digitado não é um ip ou não é um ipv4 válido.')
                        return render(request, template_name='impressora/editar.html', context=context)

            else:
                """Caso o usuário não tenha informado nada no campo ip."""
                consulta_impressora_ip = EnderecoIp.objects.filter(impressora=impressora_db)
                if consulta_impressora_ip.count() >= 1:
                    ip_antigo = consulta_impressora_ip.first()
                    ip_antigo.delete()

            # Consulta para ver se esse impressora possui um mac já cadastrado.
            consulta_impressora_mac = EnderecoMac.objects.filter(impressora=impressora_db)
            if isinstance(endereco_mac_formulario, EUI):
                if consulta_impressora_mac.count() >=1:
                    """Caso impressora já possua um mac cadastrado."""
                    mac_antigo = consulta_impressora_mac.first()
                    mac_antigo.mac_address = endereco_mac_formulario
                    mac_antigo.save()
                else:
                    mac_novo = EnderecoMac(mac_address=endereco_mac_formulario, content_type_id= impressora_objeto_tipo, parent_object_id=impressora_db.id)
                    mac_novo.save()
            else:
                if consulta_impressora_mac.count() >=1:
                    consulta_impressora_mac.delete()

            form.save()
            return redirect(impressora_view, 1)
        else:
                for valores in form.errors.values():
                    context['mensagens'].append(valores)
                
                context['field_erros'] = form.errors.keys()       
    return render(request, template_name='impressora/editar.html', context=context)


def teste_view(request):
    return render(request, template_name='teste.html')