from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http.response import JsonResponse
from django.shortcuts import get_object_or_404


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
        else:
            return JsonResponse(status=400, data={'mensagem': 'Você não pode acessar esta página. :P'}, safe=True)
