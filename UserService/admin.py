from django import forms
from django.contrib import admin
from .models import ServiceClient, User

class ServiceClientAdminSuperUserForm(forms.ModelForm):
    class Meta:
        model = ServiceClient
        fields = "__all__"


class ServiceClientAdminManagerForm(forms.ModelForm):
    class Meta:
        model = ServiceClient
        fields = ["email_verified", "full_name", "comment"]


@admin.register(ServiceClient)
class ServiceClientAdmin(admin.ModelAdmin):
    list_display = ("get_user_email", "full_name", "email_verified")
    list_filter = ("email_verified",)
    search_fields = ("user__email", "full_name")

    def get_user_email(self, obj):
        return obj.user.email if obj.user else None

    get_user_email.short_description = "Email"

    def get_form(self, request, obj=None, **kwargs):
        if request.user.is_superuser:
            return ServiceClientAdminSuperUserForm
        return ServiceClientAdminManagerForm

    def get_readonly_fields(self, request, obj=None):
        if request.user.is_superuser:
            return []
        else:
            return ["user"]

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("email", "first_name", "last_name", "is_active")
    list_filter = ("is_active",)
    search_fields = ("email", "first_name", "last_name")
