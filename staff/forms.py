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
                {'class': 'text-center mt-1 text-xs focus:outline-none border-b-2 border-cyan-700 text-cyan-800 p-2 rounded shadow-sm shadow-black hover:border-cyan-700 focus:border-cyan-700'})


class ProfileForm(forms.ModelForm):
    def clean_dob(self):
        dob = self.cleaned_data.get('dob')
        if self.instance.dob and dob != self.instance.dob:
            raise forms.ValidationError('this action is forbidden, {} is the default'.format(self.instance.dob.strftime("%m-%d-%Y")))
        return dob

    class Meta:
        model = Profile
        fields = '__all__'
        widgets = {
            'dob': forms.DateInput(attrs={'type': 'date'}),
            'nameoc': forms.Textarea(attrs={'rows': 3,'cols':10}),
            'doboc': forms.Textarea(attrs={'rows': 3,'cols':10}),
        }
        exclude = ['user', 'created', 'updated']

    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        self.fields['state'].queryset = State.objects.none()
        self.fields['lga'].queryset = LGA.objects.none()
        self.fields['senate_district'].queryset = SenateDistrict.objects.none()
        for field in self.fields.values():
            # field.required=True
            field.widget.attrs.update(
                {'class': 'text-center mt-1 text-xs focus:outline-none border-b-2 border-cyan-700 text-cyan-800 p-2 rounded shadow-sm shadow-black hover:border-cyan-700 focus:border-cyan-700'})

        if 'zone' in self.data:
            try:
                zone_id = int(self.data.get('zone'))
                self.fields['state'].queryset = State.objects.filter(zone_id=zone_id)
            except (ValueError, TypeError):
                pass

        if 'state' in self.data:
            try:
                state_id = int(self.data.get('state'))
                self.fields['lga'].queryset = LGA.objects.filter(state_id=state_id)
            except (ValueError, TypeError):
                pass

        if 'lga' in self.data:
            try:
                lga_id = int(self.data.get('lga'))
                self.fields['senate_district'].queryset = SenateDistrict.objects.filter(lga_id=lga_id)
            except (ValueError, TypeError):
                pass

        elif self.instance.pk:
            if self.instance.zone:
                self.fields['state'].queryset = self.instance.zone.state_set.order_by('name')
            if self.instance.state:
                self.fields['lga'].queryset = self.instance.state.lga_set.order_by('name')
            if self.instance.lga:
                self.fields['senate_district'].queryset = self.instance.lga.senatedistrict_set.order_by('name')


class GovtAppForm(forms.ModelForm):
    def clean_date_fapt(self):
        date_fapt = self.cleaned_data.get('date_fapt')
        if self.instance.date_fapt and date_fapt != self.instance.date_fapt:
            raise forms.ValidationError(
                f'this action is forbidden, {self.instance.date_fapt.strftime("%m-%d-%Y")} is the default date of first appointment, you cannot alter it')
        return date_fapt

    class Meta:
        model = GovernmentAppointment
        fields = ['department', 'cpost', 'ippis_no', 'date_fapt', 'date_capt', 'sfapt',
                  'salary_scale', 'grade_level', 'step', 'type_of_cadre', 'exams_status','cleared']
        widgets = {
            'date_fapt': forms.DateInput(attrs={'type': 'date'}),
            'date_capt': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super(GovtAppForm, self).__init__(*args, **kwargs)
        self.fields['department'].widget.attrs.update({'id': 'id_department', 'onchange': 'load_posts()'})
        for field in self.fields.values():
            # field.required = True
            field.widget.attrs.update({
            'class': 'text-center text-xs focus:outline-none border-b-2 border-cyan-700 text-cyan-800 p-2 rounded shadow-sm shadow-black hover:border-cyan-700 focus:border-cyan-700'
        })


class QualForm(forms.ModelForm):
    class Meta:
        model = Qualification
        fields = ['school', 'school_category', 'qual', 'date_obtained']

        widgets = {
            'date_obtained': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super(QualForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            # field.required=True
            field.widget.attrs.update(
                {'class': 'text-center mt-1 text-xs focus:outline-none border-b-2 border-cyan-700 text-cyan-800 p-2 rounded shadow-sm shadow-black hover:border-cyan-700 focus:border-cyan-700'})


class ProQualForm(forms.ModelForm):
    class Meta:
        model = ProfessionalQualification
        fields = ['institute', 'inst_address',
                  'qual_obtained', 'date_obtained']

        widgets = {
            'date_obtained': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super(ProQualForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            # field.required=True
            field.widget.attrs.update(
                {'class': 'text-center mt-1 text-xs focus:outline-none border-b-2 border-cyan-700 text-cyan-800 p-2 rounded shadow-sm shadow-black hover:border-cyan-700 focus:border-cyan-700'})


class PromotionForm(forms.ModelForm):
    class Meta:
        model = Promotion
        fields = ['department','cpost', 'prom_date', 'gl', 'step', 'inc_date', 'conf_date']

        widgets = {
            'prom_date': forms.DateInput(attrs={'type': 'date'}),
            'inc_date': forms.DateInput(attrs={'type': 'date'}),
            'conf_date': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super(PromotionForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            # field.required=True
            field.widget.attrs.update(
                {'class': 'text-center mt-1 text-xs focus:outline-none border-b-2 border-cyan-700 text-cyan-800 p-2 rounded shadow-sm shadow-black hover:border-cyan-700 focus:border-cyan-700'})


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
                {'class': 'text-center mt-1 text-xs focus:outline-none border-b-2 border-cyan-700 text-cyan-800 p-2 rounded shadow-sm shadow-black hover:border-cyan-700 focus:border-cyan-700'})


class LeaveForm(forms.ModelForm):
    class Meta:
        model = Leave
        fields = ['nature_of_leave', 'year', 'start_date',
                  'total_days', 'granted_days', 'status', 'comment']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(LeaveForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({
                'class': 'text-center mt-1 text-xs focus:outline-none border-b-2 border-cyan-700 text-cyan-800 p-2 rounded shadow-sm shadow-black hover:border-cyan-700 focus:border-cyan-700'
            })

    def clean(self):
        cleaned_data = super().clean()
        nature_of_leave = cleaned_data.get('nature_of_leave')
        year = cleaned_data.get('year')
        granted_days = cleaned_data.get('granted_days')

        if nature_of_leave and nature_of_leave.name.upper() == 'ANNUAL':
            existing_leaves = Leave.objects.filter(
                user=self.user,
                year=year,
                nature_of_leave__name__iexact='annual'
            )
            if existing_leaves.count() >= 2:
                raise ValidationError('You cannot take annual leave more than twice a year.')

            last_leave = existing_leaves.order_by('-created').first()
            if last_leave:
                remaining_days = last_leave.remain
                if granted_days > remaining_days:
                    raise ValidationError(f'You only have {remaining_days} days remaining for this year.')

        return cleaned_data
    

class ExecappForm(forms.ModelForm):
    class Meta:
        model = ExecutiveAppointment
        fields = ['department','cpost', 'date', 'status']

        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super(ExecappForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            # field.required=True
            field.widget.attrs.update(
                {'class': 'text-center mt-1 text-xs focus:outline-none border-b-2 border-cyan-700 text-cyan-800 p-2 rounded shadow-sm shadow-black hover:border-cyan-700 focus:border-cyan-700'})


class RetireForm(forms.ModelForm):
    class Meta:
        model = Retirement
        fields = ['date', 'status', 'retire']

        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super(RetireForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            # field.required=True
            field.widget.attrs.update(
                {'class': 'text-center mt-1 text-xs focus:outline-none border-b-2 border-cyan-700 text-cyan-800 p-2 rounded shadow-sm shadow-black hover:border-cyan-700 focus:border-cyan-700'})
