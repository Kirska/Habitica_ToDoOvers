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



