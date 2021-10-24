from django import forms
from django.forms import widgets
from django.forms.fields import CharField
from django.forms.widgets import Select, SelectMultiple, TextInput, Textarea
from .models import Departamento

class DepartamentoForm(forms.ModelForm):
    class Meta:
        model = Departamento
        fields = ['predio', 'departamento', 'singla_departamento', 'descricao']

    CHOICES_PREDIOS = [
        ('Prefeitura Arapoti', 'Prefeitura Municipal de Arapoti'),
        ('Col. Clotário', 'Colégio Clortário Portugal'),
        ('Col. Tel.Carneiro', 'Colégio Telemaco Carneiro'),
        ('Col. D.Zizi', 'Colégio Dona Zizi'),
        ('UBS Jd.Aratinga', 'UBS Jardim Aratinga'),
        ('UBS Jd.Ceres', 'UBS Jardim Ceres'),
        ('UBS Vila Romana', 'UBS Vila Romana'),
        ('CRAS', 'CRAS'),
        ('CREAS', 'CREAS - Centro de Referência Especializado em Assistência Social')
    ]

    predio = forms.ChoiceField(choices=CHOICES_PREDIOS, widget=Select(attrs={'class': 'form-control'}))
    departamento = forms.CharField(max_length=255, widget=TextInput(attrs={'class': 'form-control'}))
    singla_departamento = forms.CharField(max_length=5, widget=TextInput(attrs={'class': 'form-control'}), required=False)
    descricao = forms.CharField(max_length=1000, widget=Textarea(attrs={'rows':'3','class':'form-control'}), required=False)
