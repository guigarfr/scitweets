# -*- coding: utf-8 -*-
from django import forms
from . import models
from django.core.exceptions import ValidationError

from django.utils.translation import ugettext
from django import forms
from django.contrib.staticfiles.templatetags.staticfiles import static
import magic


class UploadFileForm(forms.Form):
    file = forms.FileField(
        label=ugettext('Select a file')
    )

    class Media:
        css = {
            'all': (static('dropzone/dist/dropzone.css'),)
        }
        js = (static('dropzone/dist/dropzone.js'),)

    def __init__(self, *args, **kwargs):
        super(UploadFileForm, self).__init__(*args, **kwargs)

        for key in self.fields:
            self.fields[key].widget.attrs.update(
                {'class': 'form-control',
                 'placeholder': ugettext("Select file")
                 })

class CreateAnswerForm(forms.ModelForm):
    class Meta:
        model = models.Answer
        fields = ['question', 'object_id', 'value_str', 'value_int', 'value_bool']
        widgets = {
            'question': forms.HiddenInput(),
            'object_id': forms.HiddenInput(),
            'value_bool': forms.HiddenInput()
        }

    def __init__(self, *args, **kwargs):
        super(CreateAnswerForm, self).__init__(*args, **kwargs)

        value_fields = ['value_str', 'value_int', 'value_bool']

        print dir(self), self.fields
        for name, field in self.fields.items():
            print "Field:", field, type(field)
            if name in value_fields:
                field.group = 2
            else:
                field.group = 1

        for key in self.fields:
            self.fields[key].widget.attrs.update(
                {'class': 'form-control',
                 'placeholder': ugettext("Introduce tu respuesta")
                 })

    def general_fields(self):
        return [(x, y,) for x, y in self.fields if y.group == 1]

    def value_fields(self):
        return [(x, y,) for x, y in self.fields if y.group == 2]
