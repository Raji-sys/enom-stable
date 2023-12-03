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


@admin.register(Qualification)
class QualAdmin(ImportMixin,admin.ModelAdmin):
    pass

@admin.register(ProfessionalQualification)
class QualAdmin(ImportMixin,admin.ModelAdmin):
    pass


class GovappForm(forms.ModelForm):
    pass

@admin.register(GovernmentAppointment)
class GovappAdmin(ImportMixin,admin.ModelAdmin):
    form=GovappForm
    readonly_fields=()
    exclude=()
    list_display = []
    list_filter = []
    search_fields = []
    list_per_page = 10


class PromotionForm(forms.ModelForm):
    pass

@admin.register(Promotion)
class PromotionAdmin(ImportMixin,admin.ModelAdmin):
    pass


class LeaveForm(forms.ModelForm):
    pass


@admin.register(Leave)
class LeaveAdmin(ImportMixin,admin.ModelAdmin):
    pass


class DisciplineForm(forms.ModelForm):
    pass

@admin.register(Discipline)
class DisciplineAdmin(ImportMixin,admin.ModelAdmin):
    pass


class ExecappForm(forms.ModelForm):
    pass

@admin.register(ExecutiveAppointment)
class ExecappAdmin(ImportMixin,admin.ModelAdmin):
    pass


class ReitrementForm(forms.ModelForm):
    pass

@admin.register(Retirement)
class RetireAdmin(ImportMixin,admin.ModelAdmin):
    pass