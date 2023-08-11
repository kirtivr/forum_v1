import datetime

from django import forms

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from django.forms import ModelForm

import posts.constants

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
    topics = forms.MultipleChoiceField(
        widget=forms.CheckboxSelectMultiple,
        choices=posts.constants.TOPICS_CHOICES
    )

    def clean(self):
        cleaned_data = super(NewPostForm, self).clean()
        title = cleaned_data.get('title')
        new_post = cleaned_data.get('new_post')
        topic = cleaned_data.get('topics')
        if not title:
            raise forms.ValidationError('No title given.')
        if not new_post:
            raise forms.ValidationError('Please add a post.')
        
class ReplyForm(forms.Form):
    reply = forms.CharField(widget=forms.Textarea(
        attrs={"id": "target-editor", "name": "content",
               "data-provide": "markdown", "rows": "12",
               "value": "# Enter your post here."}
    ), max_length=1000)

    def clean(self):
        cleaned_data = super(ReplyForm, self).clean()
        reply = cleaned_data.get('reply')
        if not reply:
            raise forms.ValidationError('Please add a post.')