"""Django Forms - Habitica To Do Over tool
"""
from django import forms
from .models import Tasks, Tags, Users


class TasksForm(forms.Form):
    name = forms.CharField(max_length=255)
    notes = forms.CharField(
        max_length=1000,
        widget=forms.Textarea()
    )
    priority = forms.ChoiceField(choices=Tasks.PRIORITY_CHOICES)
    days = forms.IntegerField()
    delay = forms.IntegerField()

    tags = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple(), required=False)

    def __init__(self, *args, **kwargs):
        args_super = args[1:]
        user_id = args[0]

        super(TasksForm, self).__init__(*args_super, **kwargs)

        user = Users.objects.get(user_id=user_id)

        choices = []
        for tag in Tags.objects.filter(tag_owner=user):
            choices.append((tag.tag_id, tag.tag_text))

        self.fields['tags'] = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple(), required=False,
                                                        choices=choices)
