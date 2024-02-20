from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django import forms
from .models import *
from django.contrib.auth.models import User


class CustomUserCreationForm(UserCreationForm):
    middle_name = forms.CharField(max_length=30, required=False)

    class Meta:
        model = get_user_model()
        fields = ['username', 'first_name',
                  'last_name', 'password1', 'password2']


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name']

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            # field.required=True
            field.widget.attrs.update(
                {'class': 'text-center mt-2 text-sm focus:outline-none border-b-4 border-cyan-900 text-cyan-950 py-2 rounded shadow-lg hover:border-cyan-700 focus:border-cyan-700'})


class ProfileForm(forms.ModelForm):
    def clean_dob(self):
        dob = self.cleaned_data.get('dob')
        if self.instance.dob and dob != self.instance.dob:
            raise forms.ValidationError('this action is forbidden, {} is the default'.format(
                self.instance.dob.strftime("%m-%d-%Y")))
        return dob

    class Meta:
        model = Profile
        fields = '__all__'
        widgets = {
            'zone': forms.Select(attrs={'id': 'id_zone'}),
            'state': forms.Select(attrs={'id': 'id_state'}),
            'lga': forms.Select(attrs={'id': 'id_lga'}),
            'dob': forms.DateInput(attrs={'type': 'date'})
        }
        exclude = ['user', 'created', 'updated']

    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            # field.required=True
            field.widget.attrs.update(
                {'class': 'text-center mt-2 text-sm focus:outline-none border-b-4 border-cyan-900 text-cyan-950 py-2 rounded shadow-lg hover:border-cyan-700 focus:border-cyan-700'})


class GovtAppForm(forms.ModelForm):
    def clean_date_fapt(self):
        date_fapt = self.cleaned_data.get('date_fapt')
        if self.instance.date_fapt and date_fapt != self.instance.date_fapt:
            raise forms.ValidationError(
                f'this action is forbidden, {self.instance.date_fapt.strftime("%m-%d-%Y")} is the default ')
        return date_fapt

    class Meta:
        model = GovernmentAppointment
        fields = ['department', 'cpost', 'ippis_no', 'date_fapt', 'date_capt', 'sfapt',
                  'salary_scale', 'grade_level', 'step', 'type_of_cadre', 'exams_status']
        widgets = {
            'department': forms.Select(attrs={'id': 'id_department'}),
            'current_post': forms.Select(attrs={'id': 'id_current_post'}),
            'date_fapt': forms.DateInput(attrs={'type': 'date'}),
            'date_capt': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super(GovtAppForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            # field.required=True
            field.widget.attrs.update(
                {'class': 'text-center mt-2 text-sm focus:outline-none border-b-4 border-cyan-900 text-cyan-950 py-2 rounded shadow-lg hover:border-cyan-700 focus:border-cyan-700'})


class QualForm(forms.ModelForm):
    class Meta:
        model = Qualification
        fields = ['school', 'school_category', 'qual', 'date_obtained']
        
        widgets={
            'date_obtained':forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super(QualForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            # field.required=True
            field.widget.attrs.update(
                {'class': 'text-center mt-2 text-sm focus:outline-none border-b-4 border-cyan-900 text-cyan-950 py-2 rounded shadow-lg hover:border-cyan-700 focus:border-cyan-700'})


class ProQualForm(forms.ModelForm):
    class Meta:
        model = ProfessionalQualification
        fields = ['institute', 'inst_address',
                  'qual_obtained', 'date_obtained']
        
        widgets={
            'date_obtained':forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super(ProQualForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            # field.required=True
            field.widget.attrs.update(
                {'class': 'text-center mt-2 text-sm focus:outline-none border-b-4 border-cyan-900 text-cyan-950 py-2 rounded shadow-lg hover:border-cyan-700 focus:border-cyan-700'})


class PromotionForm(forms.ModelForm):
    class Meta:
        model = Promotion
        fields = ['cpost', 'prom_date', 'gl', 'step', 'inc_date', 'conf_date']
        
        widgets={
            'prom_date':forms.DateInput(attrs={'type': 'date'}),
            'inc_date':forms.DateInput(attrs={'type': 'date'}),
            'conf_date':forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super(PromotionForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            # field.required=True
            field.widget.attrs.update(
                {'class': 'text-center mt-2 text-sm focus:outline-none border-b-4 border-cyan-900 text-cyan-950 py-2 rounded shadow-lg hover:border-cyan-700 focus:border-cyan-700'})


class DisciplineForm(forms.ModelForm):
    class Meta:
        model = Discipline
        fields = ['offense', 'decision', 'action_date', 'comment']

        widgets = {
            'action_date': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super(DisciplineForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            # field.required=True
            field.widget.attrs.update(
                {'class': 'text-center mt-2 text-sm focus:outline-none border-b-4 border-cyan-900 text-cyan-950 py-2 rounded shadow-lg hover:border-cyan-700 focus:border-cyan-700'})


class LeaveForm(forms.ModelForm):
    class Meta:
        model = Leave
        fields = ['nature', 'year', 'start_date',
                  'total_days', 'granted_days', 'status', 'comment']
        
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super(LeaveForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            # field.required=True
            field.widget.attrs.update(
                {'class': 'text-center mt-2 text-sm focus:outline-none border-b-4 border-cyan-900 text-cyan-950 py-2 rounded shadow-lg hover:border-cyan-700 focus:border-cyan-700'})


class ExecappForm(forms.ModelForm):
    class Meta:
        model = ExecutiveAppointment
        fields = ['designation', 'date', 'status']
        
        widgets={
            'date':forms.DateInput(attrs={'type': 'date'}),
        }
    def __init__(self, *args, **kwargs):
        super(ExecappForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            # field.required=True
            field.widget.attrs.update(
                {'class': 'text-center mt-2 text-sm focus:outline-none border-b-4 border-cyan-900 text-cyan-950 py-2 rounded shadow-lg hover:border-cyan-700 focus:border-cyan-700'})


class RetireForm(forms.ModelForm):
    class Meta:
        model = Retirement
        fields = ['date', 'status', 'retire', 'rtb']
        
        widgets={
            'date':forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super(RetireForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            # field.required=True
            field.widget.attrs.update(
                {'class': 'text-center mt-2 text-sm focus:outline-none border-b-4 border-cyan-900 text-cyan-950 py-2 rounded shadow-lg hover:border-cyan-700 focus:border-cyan-700'})
