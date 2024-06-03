from django import forms
from django.contrib import admin
from UserService.models import ServiceClient


class ServiceClientAdminSuperUserForm(forms.ModelForm):
    class Meta:
        model = ServiceClient
        fields = '__all__'


class ServiceClientAdminManagerForm(forms.ModelForm):
    class Meta:
        model = ServiceClient
        fields = ['is_active']


@admin.register(ServiceClient)
class ServiceClientAdmin(admin.ModelAdmin):
    list_display = ('email', 'first_name', 'last_name', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('email', 'first_name', 'last_name',)

    def get_form(self, request, obj=None, **kwargs):
        if request.user.is_superuser:
            return ServiceClientAdminSuperUserForm
        return ServiceClientAdminManagerForm

    def get_readonly_fields(self, request, obj=None):
        if request.user.is_superuser:
            return []
        else:
            return ['email', 'first_name', 'last_name']
