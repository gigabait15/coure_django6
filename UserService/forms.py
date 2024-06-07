from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import ServiceClient

class StyleFormMixin:

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs["class"] = "form-control"

class UsersRegisterForm(StyleFormMixin, UserCreationForm):

    class Meta:
        model = ServiceClient
        fields = ("user", "password1", "password2")


class UsersProfileForm(StyleFormMixin, UserChangeForm):

    class Meta:
        model = ServiceClient
        fields = ("full_name", "comment")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["password"].widget = forms.HiddenInput()