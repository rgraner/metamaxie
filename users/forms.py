from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import ScholarTeam, User

from django.shortcuts import redirect

# from allauth.account.forms import SignupForm


class LoginForm(forms.Form):
    username = forms.CharField(
        widget = forms.TextInput(
            attrs={
                'class': 'form-control'
            }
        )
    )
    password = forms.CharField(
        widget = forms.PasswordInput(
            attrs={
                'class': 'form-control'
            }
        )
    )


TYPE_CHOICES = [('MANAGER', 'Manager'), ('SCHOLAR', 'Scholar')]

class RegistrationForm(UserCreationForm):

    class Meta:
        model = User
        fields = (
            'username', 
            'email',
            'first_name',
            'last_name',
            'password1', 
            'password2',
            'type',
        )
        required = (
            'email',
            'first_name',
            'last_name',
            'type',
        )

    type = forms.ChoiceField(widget=forms.RadioSelect, choices=TYPE_CHOICES)

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        for field_name in ('username', 'email', 'password1', 'password2'):
            self.fields[field_name].help_text = ''

        for field in self.Meta.required:
            self.fields[field].required = True
        

















