from django.contrib import admin, messages
from django.core.exceptions import ValidationError
from import_export.admin import ImportMixin
from .models import * 
from django import forms



admin.site.site_header="ADMIN PANEL"
admin.site.index_title="ENOM"
admin.site.site_title="ENOM"


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ['name','created']
    list_filter = ['name']
    search_fields = ['name']
    list_per_page = 10


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['name','department','created']
    list_filter = ['name','department']
    search_fields = ['name','department']
    list_per_page = 10


@admin.register(Duties)
class DepartmentDutiesAdmin(admin.ModelAdmin):
    list_display = ['name','department']
    list_filter = ['name','department']
    search_fields = ['name','department']
    list_per_page = 10


@admin.register(Zone)
class ZoneAdmin(admin.ModelAdmin):
    list_display = ['name']
    list_filter = ['name']
    search_fields = ['name']
    list_per_page = 10

@admin.register(State)
class StateAdmin(admin.ModelAdmin):
    list_display = ['name', 'zone']
    list_filter = ['zone', 'name']
    search_fields = ['name', 'zone__name']
    list_per_page = 10

@admin.register(LGA)
class LGAAdmin(admin.ModelAdmin):
    list_display = ['name', 'state', 'get_zone']
    list_filter = ['state', 'state__zone']
    search_fields = ['name', 'state__name', 'state__zone__name']
    list_per_page = 10

    def get_zone(self, obj):
        return obj.state.zone
    get_zone.short_description = 'Zone'
    get_zone.admin_order_field = 'state__zone'

@admin.register(SenateDistrict)
class SenateDistrictAdmin(admin.ModelAdmin):
    list_display = ['name', 'lga', 'get_state', 'get_zone']
    list_filter = ['lga__state__zone', 'lga__state', 'lga']
    search_fields = ['name', 'lga__name', 'lga__state__name', 'lga__state__zone__name']
    list_per_page = 10

    def get_state(self, obj):
        return obj.lga.state
    get_state.short_description = 'State'
    get_state.admin_order_field = 'lga__state'

    def get_zone(self, obj):
        return obj.lga.state.zone
    get_zone.short_description = 'Zone'
    get_zone.admin_order_field = 'lga__state__zone'


@admin.register(Profile)
class ProfileAdmin(ImportMixin,admin.ModelAdmin):
    # form=ProfileForm
    readonly_fields=()
    exclude=()
    list_display = ['user','full_name']
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
    list_display = ['user','full_name']
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