from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django import forms
from .models import *
from django.contrib.auth.models import User


class CustomUserCreationForm(UserCreationForm):
    middle_name = forms.CharField(max_length=30, required=False)

    class Meta:
        model = get_user_model()
        fields = ['username', 'first_name', 'last_name', 'password1', 'password2']

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username','first_name','last_name']


class ProfileForm(forms.ModelForm):    
    def clean_dob(self):
        dob=self.cleaned_data.get('dob')
        if self.instance.dob and dob != self.instance.dob:
            raise forms.ValidationError('this action is forbidden, {} is the default'.format(self.instance.dob.strftime("%m-%d-%Y")))
        return dob

    class Meta:
        model = Profile
        fields = '__all__'
        widgets = {
            'zone':forms.Select(attrs={'id':'id_zone'}),
            'state':forms.Select(attrs={'id':'id_state'}),
            'lga':forms.Select(attrs={'id':'id_lga'}),
        }        
        exclude = ['user','created','updated']

class GovtAppForm(forms.ModelForm):
    def clean_date_fapt(self):
        date_fapt = self.cleaned_data.get('date_fapt')
        if self.instance.date_fapt and date_fapt != self.instance.date_fapt:
            raise forms.ValidationError(f'this action is forbidden, {self.instance.date_fapt.strftime("%m-%d-%Y")} is the default ')
        return date_fapt
    
    class Meta:
        model = GovernmentAppointment
        fields = '__all__'
        widgets = {
            'department':forms.Select(attrs={'id':'id_department'}),
            'current_post':forms.Select(attrs={'id':'id_current_post'}),
        }
        exclude = ['user','created','updated']

    def __init__(self,*args, **kwargs):
        super().__init__(*args, **kwargs)


class QualForm(forms.ModelForm):
    class Meta:
        model=Qualification
        fields='__all__'
        exclude=['user','date_obtained']


class ProQualForm(forms.ModelForm):
    class Meta:
        model=ProfessionalQualification
        fields='__all__'
        exclude=['user','qual_obtained','date_obtained']


class PromotionForm(forms.ModelForm):
    class Meta:
        model = Promotion
        fields = '__all__'
        exclude = ['user','govapp','due','inc_date','conf_date','prom_date']
