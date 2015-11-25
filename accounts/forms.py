from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms


class UserCreateForm(UserCreationForm):

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super(UserCreateForm, self).__init__(*args, **kwargs)
        self.fields['email'].required = True

        for key, field in self.fields.items():
            field.widget.attrs.update({
                'class': 'form-control',
                'placeholder': field.label
            })
            field.help_text = None
