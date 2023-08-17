import datetime

from django import forms

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from django.forms import ModelForm

import posts.constants

class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = single_file_clean(data, initial)
        return result


class FileFieldForm(forms.Form):
    file_field = MultipleFileField()

class NewPostForm(forms.Form):
    title = forms.CharField(
        required = True,
        widget=forms.TextInput(
        attrs={"name": "title",
               "class": "form-control",
               "placeholder": "Title?"}), max_length=255)
    new_post = forms.CharField(widget=forms.Textarea(
        attrs={"id": "target-editor", "name": "content",
               "data-provide": "markdown", "rows": "12",
               "value": "# Enter your post here."}
    ), max_length=1000)
    file_field = MultipleFileField()
    topics = forms.MultipleChoiceField(
        widget=forms.CheckboxSelectMultiple,
        choices=posts.constants.TOPICS_CHOICES
    )

    def clean(self):
        cleaned_data = super(NewPostForm, self).clean()
        title = cleaned_data.get('title')
        new_post = cleaned_data.get('new_post')
        topic = cleaned_data.get('topics')
        files = cleaned_data.get('file_field')
        if not title:
            raise forms.ValidationError('No title given.')
        if not new_post:
            raise forms.ValidationError('Please add a post.')
        for f in files:
            #...  Do some validation with each file.
            pass

class ReplyForm(forms.Form):
    reply = forms.CharField(widget=forms.Textarea(
        attrs={"id": "target-editor", "name": "content",
               "data-provide": "markdown", "rows": "12",
               "value": "# Enter your post here."}
    ), max_length=1000)
    file_field = MultipleFileField()

    def clean(self):
        cleaned_data = super(ReplyForm, self).clean()
        reply = cleaned_data.get('reply')
        if not reply:
            raise forms.ValidationError('Please add a post.')