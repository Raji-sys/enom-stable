from django.contrib import admin, messages
from django.core.exceptions import ValidationError
from import_export.admin import ImportMixin
from .models import * 
from django import forms


admin.site.site_header="ADMIN PANEL"
admin.site.index_title="ENOM"
admin.site.site_title="ENOM"


class ProfileForm(forms.ModelForm):
    pass
    # class Meta:
    #     model = Profile
    #     fields = []  

@admin.register(Profile)
class ProfileAdmin(ImportMixin,admin.ModelAdmin):
    form=ProfileForm
    readonly_fields=()
    exclude=()
    list_display = []
    list_filter = []
    search_fields = []
    list_per_page = 10