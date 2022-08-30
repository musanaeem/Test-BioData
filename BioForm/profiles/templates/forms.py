import imp
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .. models import Bio

class BioForm(forms.ModelForm):
    class Meta:
        model = Bio
        fields = ["user", "name", "address", "description"]
        widgets = {"user": forms.HiddenInput()}


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]