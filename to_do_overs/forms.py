"""Django Forms - Habitica To Do Over tool
"""
from django import forms
from .models import Tasks


class TasksForm(forms.Form):
    name = forms.CharField(max_length=255)
    notes = forms.CharField(
        max_length=1000,
        widget=forms.Textarea()
    )
    priority = forms.ChoiceField(choices=Tasks.PRIORITY_CHOICES)
    days = forms.IntegerField()
    delay = forms.IntegerField()

    task_tags = forms.MultipleChoiceField(required=False)

    def set_tags(self, tags_in):
        self.fields['task_tags'].choices = tags_in
