from django import forms
from users.models import User, ScholarTeam
        

class EditManagerForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'avatar',
        ]


class EditScholarForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'avatar',
        ]


class EditScholarFormMore(forms.ModelForm):
    class Meta:
        team_code = forms.ModelChoiceField(queryset=ScholarTeam.objects.all())
        model = ScholarTeam
        fields = [
            'team_code',
        ]
