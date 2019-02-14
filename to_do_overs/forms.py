"""Django Forms - Habitica To Do Over tool
"""
from django import forms
from .models import Tasks


class TasksForm(forms.ModelForm):
    class Meta:
        model = Tasks
        fields = ('name', 'notes', 'priority', 'days', 'delay')
