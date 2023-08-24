import datetime
from typing import Optional

from django import forms

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from django.forms import ModelForm

import posts.constants
import logging
logger = logging.getLogger(__name__)

class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True
    template_name = 'widgets/SimpleMultiFileAdder.html'

class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput(
            attrs = {"multiple": True}
        ))
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = single_file_clean(data, initial)
        return result

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

    def clean_file_field(self):
        data = self.cleaned_data['file_field']
        if data:
            # Do some validation here.
            pass
        return data

    def clean_title(self):
        title = self.cleaned_data.get('title')
        if not title:
            raise forms.ValidationError('No title given.')
        
        return title
    
    def clean_new_post(self):
        new_post = self.cleaned_data.get('new_post')
        #if not new_post:
        #    raise forms.ValidationError('Please add a post.')
        return new_post

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