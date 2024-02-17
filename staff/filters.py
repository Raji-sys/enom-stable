import django_filters
from django import forms
from .models import *

class StaffFilter(django_filters.FilterSet):
    file_no=django_filters.CharFilter(label='FN', field_name='file_no')

    class Meta:
        model = Profile
        fields=['file_no']

class GenFilter(django_filters.FilterSet):
    syear_of_fapt=django_filters.DateFilter(label="FIRST START",field_name="governmentappointment__date_fapt__year",lookup_expr='lte',widget=forms.DateInput(attrs={'type':'date'}),input_formats=['%d-%m-%Y', '%Y-%m-%d', '%m/%d/%Y'])
    eyear_of_fapt=django_filters.DateFilter(label="FIRST END",field_name="governmentappointment__date_fapt__year",lookup_expr='gt',widget=forms.DateInput(attrs={'type':'date'}),input_formats=['%d-%m-%Y', '%Y-%m-%d', '%m/%d/%Y'])
    year_of_fapt=django_filters.NumberFilter(label="C_YEAR",field_name="governmentappointment__date_fapt__year",lookup_expr='exact')

    syear_of_capt=django_filters.DateFilter(label="CURRRENT START",field_name="governmentappointment__date_capt__year",lookup_expr='lte',widget=forms.DateInput(attrs={'type':'date'}),input_formats=['%d-%m-%Y', '%Y-%m-%d', '%m/%d/%Y'])
    eyear_of_capt=django_filters.DateFilter(label="CURRENT END",field_name="governmentappointment__date_capt__year",lookup_expr='gt',widget=forms.DateInput(attrs={'type':'date'}),input_formats=['%d-%m-%Y', '%Y-%m-%d', '%m/%d/%Y'])
    year_of_capt=django_filters.NumberFilter(label="C_YEAR",field_name="governmentappointment__date_capt__year",lookup_expr='exact')

    dep=django_filters.CharFilter(label="DEPARTMENT",field_name="governmentappointment__department",lookup_expr='iexact')
    cadre=django_filters.CharFilter(label="CADRE",field_name="governmentappointment__cpost",lookup_expr='iexact')
  
    zone=django_filters.CharFilter(label="ZONE",field_name="profile__zone",lookup_expr='iexact')
    state=django_filters.CharFilter(label="STATE",field_name="profile__state",lookup_expr='iexact')
    lga=django_filters.CharFilter(label="LGA",field_name="profile__lga",lookup_expr='iexact')

    qual=django_filters.CharFilter(label="QUALIFICATION",field_name="qualification__qual",lookup_expr='iexact')
    pro_qual=django_filters.CharFilter(label="PRO QUALIFICATION",field_name="professionalqualification__qual_obtained",lookup_expr='iexact')
  
    type_of_cadre=django_filters.CharFilter(label="TYPE",field_name="governmentappointment__type_of_cadre",lookup_expr='iexact')
    due=django_filters.CharFilter(label="DUE",field_name="promotion__due",lookup_expr='iexact')
    due=django_filters.CharFilter(label="GL",field_name="governmentappointment__grade_level",lookup_expr='iexact')
    due=django_filters.NumberFilter(label="STEP",field_name="governmentappointment__step",lookup_expr='iexact')
    due=django_filters.CharFilter(label="EXAMS",field_name="governmentappointment__exam_status",lookup_expr='iexact')
  
    rt=django_filters.CharFilter(label="RETIRE",field_name="retirement__retire",lookup_expr="iexact")
    
    class Meta:
        model = User
        exclude=['first_name','password','date_joined','last_login','superuser_status','groups',
                 'user_permissions','email','last_name','username','is_superuser','is_active','is_staff']


class GovFilter(django_filters.FilterSet):
    ippis_no=django_filters.NumberFilter(label="IPPIS NUMBER",field_name="ippis_no",lookup_expr="exact")
    department=django_filters.CharFilter(label='DEPARTMENT',field_name="department",lookup_expr="iexact")
    current_post=django_filters.CharFilter(label='CURRENT POST',field_name="cpost",lookup_expr="iexact")
    
    date_of_fapt=django_filters.NumberFilter(label="DATE OF 1ST APPT",field_name="date_fapt__year",lookup_expr='exact')
    date_of_fapt1=django_filters.DateFilter(label="DATE OF 1ST APPT 1",field_name="date_fapt__year",lookup_expr='lte',widget=forms.DateInput(attrs={'type':'date'}),input_formats=['%d-%m-%Y', '%Y-%m-%d', '%m/%d/%Y'])
    date_of_fapt2=django_filters.DateFilter(label="DATE OF 1ST APPT 2",field_name="ate_fapt__year",lookup_expr='gt',widget=forms.DateInput(attrs={'type':'date'}),input_formats=['%d-%m-%Y', '%Y-%m-%d', '%m/%d/%Y'])
    
    date_of_capt=django_filters.NumberFilter(label="DATE OF CURRENT APPT",field_name="date_capt__year",lookup_expr='exact')
    date_of_capt1=django_filters.DateFilter(label="DATE OF CURRRENT APPT 1",field_name="date_capt__year",lookup_expr='lte',widget=forms.DateInput(attrs={'type':'date'}),input_formats=['%d-%m-%Y', '%Y-%m-%d', '%m/%d/%Y'])
    date_of_capt2=django_filters.DateFilter(label="DATE OF CURRENT APPT 2",field_name="date_capt__year",lookup_expr='gt',widget=forms.DateInput(attrs={'type':'date'}),input_formats=['%d-%m-%Y', '%Y-%m-%d', '%m/%d/%Y'])

    type_of_appt=django_filters.CharFilter(label="TYPE OF APPT",field_name="type_of_appt",lookup_expr="iexact")
    type_of_cadre=django_filters.CharFilter(label="TYPE OF CADRE",field_name="type_of_cadre",lookup_expr="iexact")

    salary_scale=django_filters.CharFilter(label="SALARY SCALE",field_name="salary_scale",lookup_expr="iexact")
    grade_level=django_filters.CharFilter(label="GL",field_name="grade_level",lookup_expr="iexact")
    step=django_filters.NumberFilter(label="step",field_name="step",lookup_expr="iexact")

    class Meta:
        model=GovernmentAppointment
        fields=['department','cpost','ippis_no','date_fapt','date_capt','type_of_appt','salary_scale','step','type_of_cadre']