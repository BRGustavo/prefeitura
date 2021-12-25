from django.http.response import JsonResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required, permission_required
from account.models import CustomizadoUserModel
from departamento.models import Funcionario
from dispositivo.models import Computador, Roteador, Impressora
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.contrib.auth.forms import UserCreationForm

@login_required
def admin_home(request):
    return render(request, template_name='administracao/home.html')

@login_required
def admin_usuarios(request):
    User = get_user_model()
    data = {
        'funcionario': Funcionario.objects.all().count(),
        'impressora': Impressora.objects.all().count(),
        'roteador': Roteador.objects.all().count(),
        'computador': Computador.objects.all().count(),
        'usuarios':  User.objects.all(),
        'grupos': Group.objects.all(),
        'formUsuario': UserCreationForm(),
    }
    
    return render(request, template_name='administracao/usuarios.html', context=data)