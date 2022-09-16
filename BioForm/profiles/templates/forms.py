from django import forms
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .. models import Bio, Account, Blog

class DateInput(forms.DateInput):
    input_type = 'date'

class BioForm(forms.ModelForm):
    class Meta:
        model = Bio
        fields = ["user", "name", "address", "description"]
        widgets = {"user": forms.HiddenInput()}

class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ["user", "title", "content"]
        widgets = {"user": forms.HiddenInput()}


class CreateUserForm(UserCreationForm):
    class Meta:
        model = Account
        fields = ["username", "email", "date_of_birth", "password1", "password2"]
        widgets = {"date_of_birth": DateInput()}