from django.urls import path
from .forms import LoginForm
from django.contrib.auth import views

urlpatterns = [
    path('login/', views.LoginView.as_view(redirect_authenticated_user=True, template_name='registration/login.html', authentication_form=LoginForm), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout')
]
