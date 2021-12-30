from django import forms
from django.utils.translation import templatize

from .models import Scholarship, Ronin
from users.models import Scholar, ScholarTeam, ManagerTeam


class EditScholarshipForm(forms.ModelForm):
    class Meta:
        model = Scholarship
        fields = ['scholar']
        labels = {
            # 'scholar':'scholar',
            }

    def __init__(self, *args, **kwargs):
        super(EditScholarshipForm, self).__init__(*args, **kwargs)
        manager = ManagerTeam.objects.get(manager=self.instance.owner)
        scholars = list(ScholarTeam.objects.filter(team_code=manager.id))
        self.fields['scholar'].queryset = Scholar.objects.filter(username__in=scholars)


class RoninForm(forms.ModelForm):
    class Meta:
        model = Ronin
        fields = ['ronin']
        labels = {'ronin': ''}

    def __init__(self, *args, **kwargs):
        super(RoninForm, self).__init__(*args, **kwargs)
        self.fields['ronin'].widget.attrs['placeholder'] = 'ronin:xxxx...'

    def clean_ronin_address(self):
        ronin = self.cleaned_data['ronin']

        if Ronin.objects.filter(ronin=ronin).exists():
            raise forms.ValidationError('ronin address already exists.')
        return ronin





        


