from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.forms.widgets import PasswordInput, TextInput

class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=TextInput(attrs={'class':'form-control border border-dark text-light bg-transparent','placeholder': 'Nome de usário', 'autocomplete':'off'}))
    password = forms.CharField(widget=PasswordInput(attrs={'class':'form-control border border-dark text-light bg-transparent', 'placeholder':'Senha', 'autocomplete':'off'}))

