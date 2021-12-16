from django import forms

from .models import Task
from users.models import ManagerTeam, ScholarTeam


class AddTaskForm1(forms.ModelForm):
    class Meta:
        model = Task
        fields = [
            'name',
            'task_1', 
            'rate_1',
            'fixed_rate',
            'rate_2',
            ]
        labels = {
            'name': '',
            'task_1':'',
            'rate_1':'',
            'fixed_rate':'',
            'rate_2':'',
            }


class AddTaskForm2(forms.ModelForm):
    class Meta:
        model = Task
        fields = [
            'name',
            'task_1',
            'task_2',
            'task_3',
            'task_4',
            'rate_1',
            'fixed_rate',
            'rate_2',
            'rate_3',
            'rate_4',
            'rate_5',
            ]
        labels = {
            'name':'',
            'task_1':'',
            'task_2':'',
            'task_3':'',
            'task_4':'',
            'rate_1':'',
            'fixed_rate':'',
            'rate_2':'',
            'rate_3':'',
            'rate_4':'',
            'rate_5':'',
            }


class EditTaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = [
            'scholar',
            ]
        labels = {
            'scholar': 'scholars',
            }

    def __init__(self, *args, **kwargs):
        super(EditTaskForm, self).__init__(*args, **kwargs)
        manager = ManagerTeam.objects.get(manager=self.instance.owner)
        self.fields['scholar'].queryset = ScholarTeam.objects.filter(team_code=manager.id)
         
    scholar = forms.ModelMultipleChoiceField(
        queryset = ScholarTeam.objects.all(),
        widget=forms.CheckboxSelectMultiple
        )





