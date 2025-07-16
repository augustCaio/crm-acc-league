from django import forms
from .models import Team, Event

class TeamForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = ['name']

class UploadFileForm(forms.Form):
    event = forms.ModelChoiceField(queryset=Event.objects.all(), label="Selecione o Evento")
    file = forms.FileField(label="Arquivo de Resultado (.json)") 