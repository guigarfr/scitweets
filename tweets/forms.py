# -*- coding: utf-8 -*-
from django import forms
from .models import TweetYesNoAnswer


NA_YES_NO = ((None, 'Inclasificable'), (True, 'Sí'), (False, 'No'))


class TweetQuestionForm(forms.ModelForm):
    class Meta:
        model = TweetYesNoAnswer
        fields = ['tweet', 'result']
        widgets = {
            'tweet': forms.HiddenInput(),
            'result': forms.HiddenInput()
        }