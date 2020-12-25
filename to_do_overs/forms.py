"""Django Forms - Habitica To Do Over tool
"""
from builtins import object
from django import forms
from .models import Tasks, Tags, Users


class TasksModelForm(forms.ModelForm):
    class Meta(object):
        model = Tasks
        fields = ['name', 'notes', 'priority', 'days', 'delay', 'tags']

    tags = forms.ModelMultipleChoiceField(queryset=Tags.objects.all())

    def __init__(self, *args, **kwargs):
        args_super = args[1:]
        user_id = args[0]

        super(TasksModelForm, self).__init__(*args_super, **kwargs)

        # make fields more explanatory
        self.fields['days'].label = (
            u'Number of days allotted to complete task' +
            u' (enter 0 for no due date)'
        )
        self.fields['delay'].label = (
            u'Number of days to delay before re-creating' +
            u' task (enter 0 for no delay)'
        )

        # get the list of tags for that user
        user = Users.objects.get(user_id=user_id)

        self.fields['tags'] = forms.ModelMultipleChoiceField(
            required=False,
            queryset=Tags.objects.filter(tag_owner=user)
        )
