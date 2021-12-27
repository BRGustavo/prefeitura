from django.contrib.auth import login
from django.contrib.auth.backends import UserModel
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User, Permission
from django.http.response import JsonResponse
from django.shortcuts import get_object_or_404

from account.models import CustomizadoUserModel


@login_required
def remover_usuario_ajax(request):
    if request.method == 'GET':
        if request.is_ajax():
            id_usuario = request.GET.get('id')
            usuario = get_object_or_404(User, pk=id_usuario)
            if usuario:
                if usuario.is_superuser:
                    return JsonResponse(status=400, data={'mensagem': 'Você não pode remover um superusuário'}, safe=False)
                else:
                    usuario.delete()
                    return JsonResponse(status=200, data={'mensagem': 'Removido com sucesso.'}, safe=True)
    return JsonResponse(status=400, data={'mensagem': 'Você não pode acessar esta página. :P'}, safe=True)

@login_required
def adicionar_usuario_ajax(request):
    if request.method == 'POST':
        mensagens = []
        campo_erros = []
        usuario = UserCreationForm(request.POST)
        if usuario.is_valid():
            usuario.save()
            return JsonResponse(status=200, data={'mensagem': 'ok'}, safe=True)
        else:
            for valores in usuario.errors.values():
                mensagens.append(valores)
            for campo in usuario:
                if campo.errors:
                    campo_erros.append(campo.id_for_label)
            
    return JsonResponse(status=404, data={'status':'false','mensagem': mensagens, 'field_erros': campo_erros})


@login_required
def dados_usuario_ajax(request):
    if request.method == 'GET':
        id = request.GET.get('id')
        usuario = User.objects.filter(id=id).first()
        data = {
            'corpo': {
                'id_first_name': usuario.first_name,
                'id_last_name': usuario.last_name,
                'id_email': usuario.email,
                'id_usuario': usuario.id,
            },
            'fora': {
                'id_usernamem': usuario.username,
                'id_emailm': usuario.email,
                'nome_usuario': f'{usuario.first_name} {usuario.last_name}'
            }
            
        }
        retornar = dict()

        lista_add = ['add_funcionario', 'add_computador', 'add_roteador', 'add_impressora', 'delete_funcionario', 'delete_computador', 'delete_roteador', 'delete_impressora', 'change_funcionario', 'change_computador', 'change_impressora', 'change_roteador', 'view_funcionario', 'view_computador', 'view_roteador', 'view_impressora']

            
        for permissao in usuario.user_permissions.all():
            if permissao.codename in lista_add:
                retornar[permissao.codename] = True
            
        data['campos'] = retornar

        return JsonResponse(status=200, data=data, safe=True)


@login_required
def editar_usuario_ajax(request):
    if request.method == 'GET':
        mensagens = []
        campo_erros = []
        id_usuario = request.GET.get('id_usuario')
        usuario = get_object_or_404(User, pk=id_usuario)
        if usuario:
            lista_add = ['add_funcionario', 'add_computador', 'add_roteador', 'add_impressora', 'delete_funcionario', 'delete_computador', 'delete_roteador', 'delete_impressora', 'change_funcionario', 'change_computador', 'change_impressora', 'change_roteador', 'view_funcionario', 'view_computador', 'view_roteador', 'view_impressora']

            funcao_verificar_nulo = lambda x: True if x is not None and len(x) >=1 else False

            first_name = request.GET.get('first_name')
            last_name = request.GET.get('last_name')
            email = request.GET.get('email')

            
            if funcao_verificar_nulo(first_name) and funcao_verificar_nulo(last_name) and funcao_verificar_nulo(email):
                usuario.first_name = first_name
                usuario.last_name = last_name
                usuario.email = email
                usuario.save()
                
                for valor in lista_add:
                    permissao = Permission.objects.get(codename=valor)
                    usuario.user_permissions.remove(permissao)
                for item in request.GET:
                    if item[0] == 'c':
                        valor = item[1:]
                        if valor in lista_add:
                            permissao = Permission.objects.get(codename=valor)
                            usuario.user_permissions.add(permissao)

                return JsonResponse(status=200, data={'mensagem': 'ok'}, safe=True)
            else:
                mensagens.append('Campo inválido.')
                campo_erros.append('id_first_name') if funcao_verificar_nulo(first_name) is False else None
                campo_erros.append('id_last_name') if funcao_verificar_nulo(last_name) is False else None
                campo_erros.append('id_email') if funcao_verificar_nulo(email) is False else None

            for item in request.GET:
                print(request.GET.get(item))
        else:
            mensagens.append('Usuário não existe.')
            campo_erros.append('id_first_name')
            
    return JsonResponse(status=404, data={'status':'false','mensagem': mensagens, 'field_erros': campo_erros})
