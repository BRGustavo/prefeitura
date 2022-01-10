from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from dispositivo.views import computador_view

@login_required
def index(request):

    return redirect(computador_view, 1)