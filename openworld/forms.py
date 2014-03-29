from django import forms
from django.contrib.auth.models import User
from openworld.models import Source

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'password')

class RequestForm(forms.Form):
    sources = Source.objects.all()
    source = forms.ModelChoiceField(queryset=sources, label="Source:")
    file = forms.FileField(label="File:")

class NewRequestForm(forms.Form):
    source = forms.CharField(required=True)
    url = forms.URLField(required=False)
    file = forms.FileField(label="File:")
