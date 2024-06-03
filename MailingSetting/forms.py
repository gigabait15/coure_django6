from django import forms
from MailingSetting.models import MailingSetting, MessageMailing


class StyleFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class MailingSettingForm(StyleFormMixin, forms.ModelForm):

    class Meta:
        model = MailingSetting
        exclude = ('created_by', 'first_send_datetime',)
        widgets = {
            'client': forms.CheckboxSelectMultiple,
        }


class MailingMessageForm(StyleFormMixin, forms.ModelForm):

    class Meta:
        model = MessageMailing
        fields = ('letter_subject', 'letter_body')
