from django.shortcuts import render, get_object_or_404, HttpResponseRedirect
from django.views.generic.edit import UpdateView, CreateView, DeleteView
from django.views.generic.base import TemplateView
from django.views.generic import DetailView, ListView
from django.views import View
from .forms import CustomUserCreationForm
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.views import LoginView, LogoutView
from django.http import HttpResponse
from .models import *
from .forms import *
from .filters import *
from django.contrib.auth import get_user_model
from io import BytesIO
from django.template.loader import get_template
from xhtml2pdf import pisa
import datetime
from django.conf import settings
import os
import csv
from django.db.models import Count
User = get_user_model()


def log_anonymous_required(view_function, redirect_to=None):
    if redirect_to is None:
        redirect_to = '/'
    return user_passes_test(lambda u: not u.is_authenticated, login_url=redirect_to)(view_function)


@login_required
def fetch_resources(uri, rel):
    """
    Handles fetching static and media resources when generating the PDF.
    """
    if uri.startswith(settings.STATIC_URL):
        path = os.path.join(settings.STATIC_ROOT,
                            uri.replace(settings.STATIC_URL, ""))
    else:
        path = os.path.join(settings.MEDIA_ROOT,
                            uri.replace(settings.MEDIA_URL, ""))
    return path


@method_decorator(login_required(login_url='login'), name='dispatch')
class IndexView(TemplateView):
    template_name = "index.html"


@login_required
def manage(request):
    return render(request, 'manage.html')


@method_decorator(login_required(login_url='login'), name='dispatch')
class StaffListView(ListView):
    model = Profile
    template_name = "staff/stafflist.html"
    context_object_name = 'profiles'
    paginate_by = 10

    def get_queryset(self):
        profiles = super().get_queryset().order_by(
            'user__governmentappointment__department')
        staff_filter = StaffFilter(self.request.GET, queryset=profiles)
        return staff_filter.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        total_profiles = self.get_queryset().count()
        context['staffFilter'] = StaffFilter(
            self.request.GET, queryset=self.get_queryset())
        context['total_profiles'] = total_profiles
        return context


@login_required
def dept(request):
    return render(request, 'dept.html')


@login_required
def dept_details(request):
    pass


@login_required
def dirs(request):
    return render(request, 'dirs.html')


@login_required
def dirs_details(request):
    pass


@login_required
def report(request):
    return render(request, 'report.html')


@method_decorator(login_required(login_url='login'), name='dispatch')
class GenReportView(ListView):
    model = get_user_model()
    template_name = 'staff/report/gen_report.html'
    paginate_by = 10
    context_object_name = 'users'

    def get_queryset(self):
        queryset = super().get_queryset()
        total = queryset.filter(is_active=True, is_superuser=False).count()

        gen_filter = GenFilter(self.request.GET, queryset=queryset)
        users = gen_filter.qs.order_by('governmentappointment__department')

        self.total = total
        return users

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['gen_filter'] = GenFilter(
            self.request.GET, queryset=self.get_queryset())
        context['total'] = self.total
        return context


@login_required
def Gen_pdf(request):
    ndate = datetime.datetime.now()
    filename = ndate.strftime('on_%d/%m/%Y_at_%I.%M%p.pdf')
    f = GenFilter(request.GET, queryset=User.objects.all()).qs

    result = ""
    for key, value in request.GET.items():
        if value:
            result += f" {value.upper()}<br>Generated on: {ndate.strftime('%d-%B-%Y at %I:%M %p')}</br>By: {request.user.username.upper()}"

    context = {'f': f, 'pagesize': 'A4',
               'orientation': 'landscape', 'result': result}
    response = HttpResponse(content_type='application/pdf',
                            headers={'Content-Disposition': f'filename="Report__{filename}"'})

    buffer = BytesIO()

    pisa_status = pisa.CreatePDF(get_template('staff/report/gen_pdf.html').render(
        context), dest=buffer, encoding='utf-8', link_callback=fetch_resources)

    if not pisa_status.err:
        pdf = buffer.getvalue()
        buffer.close()
        response.write(pdf)
        return response
    return HttpResponse('Error generating PDF', status=500)


@login_required
def Gen_csv(request):
    ndate = datetime.datetime.now()
    filename = ndate.strftime('on_%d/%m/%Y_at_%I.%M%p.csv')
    response = HttpResponse(content_type='text/csv', headers={
                            'Content-Disposition': f'attachment; filename="generated_by_{request.user}_{filename}"'})
    user = User.objects.all()
    genFilter = GenFilter(request.GET, queryset=user)
    user = genFilter.qs
    # result=request.GET['date_of_first_appointment']
    writer = csv.writer(response)
    # csv headers
    # writer.writerow(['','','','','','','Data of {} staff'.format(result) ])
    writer.writerow([
                    'S/N', 'FULLNAME', 'FILE NO', 'IPPIS NUMBER', 'SEX', 'DEPARTMENT', 'CURRENT POST', 'DATE OF FIRST APPOINTMENT'])

    # generate csv body data with variables using foor loop
    for i, u in enumerate(user, start=1):

        writer.writerow([
            i,
            str(u.first_name).upper()+str(' ') +
            str(u.profile.middle_name).upper() +
            str(' ')+str(u.last_name).upper(),
            u.profile.file_no,
            u.governmentappointment.ippis_no,
            str(u.profile.gender).upper(),
            str(u.governmentappointment.department).upper(),
            str(u.governmentappointment.cpost).upper(),
            u.governmentappointment.date_fapt,
        ])
    return response


@method_decorator(login_required(login_url='login'), name='dispatch')
class GovReportView(ListView):
    model = GovernmentAppointment
    template_name = 'staff/report/gov_report.html'
    paginate_by = 10
    context_object_name = 'gov'

    def get_queryset(self):
        queryset = super().get_queryset()
        # total = queryset.filter(is_active=True, is_superuser=False).count()

        gov_filter = GovFilter(self.request.GET, queryset=queryset)
        gov = gov_filter.qs.order_by('department')

        # self.total = total
        return gov

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['gov_filter'] = GovFilter(
            self.request.GET, queryset=self.get_queryset())
        # context['total'] = self.total
        return context


@login_required
def Gov_pdf(request):
    ndate = datetime.datetime.now()
    filename = ndate.strftime('on_%d/%m/%Y_at_%I.%M%p.pdf')
    f = GovFilter(request.GET, queryset=GovernmentAppointment.objects.all()).qs

    result = ""
    for key, value in request.GET.items():
        if value:
            result += f" {value.upper()}<br>Generated on: {ndate.strftime('%d-%B-%Y at %I:%M %p')}</br>By: {request.user.username.upper()}"

    context = {'f': f, 'pagesize': 'A4',
               'orientation': 'potrait', 'result': result}
    response = HttpResponse(content_type='application/pdf',
                            headers={'Content-Disposition': f'filename="Report__{filename}"'})

    buffer = BytesIO()

    pisa_status = pisa.CreatePDF(get_template('staff/report/gov_pdf.html').render(
        context), dest=buffer, encoding='utf-8', link_callback=fetch_resources)

    if not pisa_status.err:
        pdf = buffer.getvalue()
        buffer.close()
        response.write(pdf)
        return response
    return HttpResponse('Error generating PDF', status=500)


@login_required
def Gov_csv(request):
    ndate = datetime.datetime.now()
    filename = ndate.strftime('on_%d/%m/%Y_at_%I.%M%p.csv')
    response = HttpResponse(content_type='text/csv', headers={
                            'Content-Disposition': f'attachment; filename="generated_by_{request.user}_{filename}"'})
    gov = GovernmentAppointment.objects.all()
    govFilter = GovFilter(request.GET, queryset=gov)
    gov = genFilter.qs
    # result=request.GET['date_of_first_appointment']
    writer = csv.writer(response)
    # csv headers
    # writer.writerow(['','','','','','','Data of {} staff'.format(result) ])
    writer.writerow([
                    'S/N', 'FULLNAME', 'FILE NO', 'IPPIS NUMBER', 'DEPARTMENT', 'CURRENT POST', 'DATE OF FIRST APPOINTMENT', 'DATE OF CURRENT APPOINTMENT'])

    # generate csv body data with variables using foor loop
    for i, u in enumerate(user, start=1):

        writer.writerow([
            i,
            str(u.first_name).upper()+str(' ') +
            str(u.profile.middle_name).upper() +
            str(' ')+str(u.last_name).upper(),
            u.profile.file_no,
            u.governmentappointment.ippis_no,
            str(u.profile.gender).upper(),
            str(u.governmentappointment.department).upper(),
            str(u.governmentappointment.cpost).upper(),
            u.governmentappointment.date_fapt,
        ])
    return response


@login_required
def pro_report(request):
    pass
    # return render(request, 'pro_report.html')


@login_required
def lv_report(request):
    pass
    # return render(request, 'lv_report.html')


@login_required
def dis_report(request):
    pass
    # return render(request, 'dis_report.html')


@login_required
def qual_report(request):
    pass
    # return render(request, 'qual_report.html')


@login_required
def pro_qual_report(request):
    pass
    # return render(request, 'pro_qual_report.html')


@login_required
def rt_report(request):
    pass
    # return render(request, 'rt_report.html')


@method_decorator(login_required(login_url='login'), name='dispatch')
class StatsView(TemplateView):
    template_name = 'stats.html'

    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)

        pc = Profile.objects.all().count()
        gender_counts = Profile.objects.values('gender').annotate(pc=Count('id'))
        geo_counts = Profile.objects.values('zone').annotate(pc=Count('id'))
        state_counts = Profile.objects.values('state').annotate(pc=Count('id'))
        lga_counts = Profile.objects.values('lga').annotate(pc=Count('id'))
        religion_counts = Profile.objects.values('religion').annotate(pc=Count('id'))
        ms_counts = Profile.objects.values('marital_status').annotate(pc=Count('id'))
        tc_counts = GovernmentAppointment.objects.values('type_of_cadre').annotate(pc=Count('id'))
        department_counts = GovernmentAppointment.objects.values('department').annotate(pc=Count('id'))
        cpost_counts = GovernmentAppointment.objects.values('cpost').annotate(pc=Count('id'))
        ss_counts = GovernmentAppointment.objects.values('salary_scale').annotate(pc=Count('id'))
        gl_counts = GovernmentAppointment.objects.values('grade_level').annotate(pc=Count('id'))
        sc_counts = Qualification.objects.values('school_category').annotate(pc=Count('id'))
        context['pc'] = pc
        context['gender_counts'] = gender_counts
        context['geo_counts'] = geo_counts
        context['state_counts'] = state_counts
        context['lga_counts'] = lga_counts
        context['religion_counts'] = religion_counts
        context['ms_counts'] = ms_counts
        context['tc_counts'] = tc_counts
        context['department_counts'] = department_counts
        context['cpost_counts'] = cpost_counts
        context['ss_counts'] = ss_counts
        context['gl_counts'] = gl_counts
        context['sc_counts'] = sc_counts

        return context


@method_decorator(login_required(login_url='login'), name='dispatch')
class NoticeView(TemplateView):
    template_name='notice.html'

    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)

        due_appts=GovernmentAppointment.objects.filter(due=True).select_related('user__profile')
        retire_st= GovernmentAppointment.objects.filter(retire=True).select_related('user__profile') 
        leave_st=Leave.objects.filter(is_leave_over=True).select_related('user__profile')

        context.update({
            'due_count':due_appts.count(),
            'retire_count':retire_st.count(),
            'leave_count':leave_st.count(),
            'due_appts':due_appts,
            'retire_st':retire_st,
            'leave_st':leave_st
        })
        return context

@method_decorator(log_anonymous_required, name='dispatch')
class CustomLoginView(LoginView):
    template_name = 'login.html'

    def get_success_url(self):
        if self.request.user.is_superuser:
            return reverse_lazy('index')
        else:
            return reverse_lazy('profile_details', args=[self.request.user.username])


@method_decorator(login_required(login_url='login'), name='dispatch')
class CustomLogoutView(LogoutView):
    template_name = 'login.html'

    def dispatch(self, request, *args, **kwargs):
        response = super().dispatch(request, *args, **kwargs)
        messages.success(request, 'logout successful')
        return response


def reg_anonymous_required(view_function, redirect_to=None):
    if redirect_to is None:
        redirect_to = '/'
    return user_passes_test(lambda u: not u.is_authenticated or u.is_superuser, login_url=redirect_to)(view_function)


@method_decorator(reg_anonymous_required, name='dispatch')
class UserRegistrationView(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'registration/register.html'
    success_url = ""

    def form_valid(self, form):
        if form.is_valid():
            response = super().form_valid(form)
            user = User.objects.get(username=form.cleaned_data['username'])
            profile_instance = Profile(user=user)
            profile_instance.save()
            govapp_instance = GovernmentAppointment(user=user)
            govapp_instance.save()
            messages.success(
                self.request, f"Registration for: {user.get_full_name()} was successful")
            return response
        else:
            print("Form errors:", form.errors)
            return self.form_invalid(form)

    def get_success_url(self):
        if self.request.user.is_superuser:
            return reverse_lazy('staff')
        else:
            return reverse_lazy('index')


@method_decorator(reg_anonymous_required, name='dispatch')
class UserRegView(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'registration/reg.html'
    success_url = ""

    def form_valid(self, form):
        if form.is_valid():
            response = super().form_valid(form)
            user = User.objects.get(username=form.cleaned_data['username'])
            profile_instance = Profile(user=user)
            profile_instance.save()
            govapp_instance = GovernmentAppointment(user=user)
            govapp_instance.save()
            messages.success(
                self.request, f"Registration for: {user.get_full_name()} was successful")
            return response
        else:
            print("Form errors:", form.errors)
            return self.form_invalid(form)

    def get_success_url(self):
        if self.request.user.is_superuser:
            return reverse_lazy('staff')
        else:
            return reverse_lazy('index')


@method_decorator(login_required(login_url='login'), name='dispatch')
class DocumentationView(UpdateView):
    model = User
    template_name = 'doc.html'
    form_class = UserForm
    success_url = reverse_lazy('staff')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profileform'] = ProfileForm(instance=self.object.profile)
        context['govtappform'] = GovtAppForm(
            instance=self.object.governmentappointment)
        return context

    def form_valid(self, form):
        userform = UserForm(self.request.POST, instance=self.object)
        profileform = ProfileForm(
            self.request.POST, instance=self.object.profile)
        govtappform = GovtAppForm(
            self.request.POST, instance=self.object.governmentappointment)

        if userform.is_valid() and profileform.is_valid() and govtappform.is_valid():
            userform.save()
            profileform.save()
            govtappform.save()
            messages.success(
                self.request, f'Documentation successful!{self.request.user.last_name}')
            return HttpResponseRedirect(self.get_success_url())
        else:
            messages.error(
                self.request, 'Please correct the errors to proceed')
            return self.form_invalid(form)


@method_decorator(login_required(login_url='login'), name='dispatch')
class UpdateUserView(UpdateView):
    model = User
    template_name = 'staff/update-user.html'
    form_class = UserForm
    success_url = reverse_lazy('profile_details')

    def get_success_url(self):
        messages.success(
            self.request, 'Staff Information Updated Successfully')
        return reverse_lazy('profile_details', kwargs={'username': self.object.username})

    def form_valid(self, form):
        if form.is_valid():
            form.save()
            return super().form_valid(form)
        else:
            return self.form_invalid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'error updating staff information')
        return self.render_to_response(self.get_context_data(form=form))


@method_decorator(login_required(login_url='login'), name='dispatch')
class UpdateProfileView(UpdateView):
    model = Profile
    template_name = 'staff/update-profile.html'
    form_class = ProfileForm
    success_url = reverse_lazy('profile_details')

    def get_success_url(self):
        messages.success(
            self.request, 'Staff Information Updated Successfully')
        return reverse_lazy('profile_details', kwargs={'username': self.object.user})

    def form_valid(self, form):
        if form.is_valid():
            form.save()
            return super().form_valid(form)
        else:
            return self.form_invalid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'error updating staff information')
        return self.render_to_response(self.get_context_data(form=form))


@method_decorator(login_required(login_url='login'), name='dispatch')
class UpdateGovappView(UpdateView):
    model = GovernmentAppointment
    template_name = 'staff/update-govapp.html'
    form_class = GovtAppForm
    success_url = reverse_lazy('profile_details')

    def get_success_url(self):
        messages.success(
            self.request, 'Staff Information Updated Successfully')
        return reverse_lazy('profile_details', kwargs={'username': self.object.user})

    def form_invalid(self, form):
        messages.error(self.request, 'error updating staff information')
        return self.render_to_response(self.get_context_data(form=form))


@method_decorator(login_required(login_url='login'), name='dispatch')
class ProfileDetailView(DetailView):
    template_name = 'staff/profile_details.html'
    model = Profile

    def get_object(self, queryset=None):
        if self.request.user.is_superuser:
            username_from_url = self.kwargs.get('username')
            user = get_object_or_404(User, username=username_from_url)
        else:
            user = self.request.user
        return get_object_or_404(Profile, user=user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = context['object']

        qualifications = Qualification.objects.filter(user=profile.user)
        pro_qualifications = ProfessionalQualification.objects.filter(
            user=profile.user)
        promotion = Promotion.objects.filter(user=profile.user)
        discipline = Discipline.objects.filter(user=profile.user)
        leave = Leave.objects.filter(user=profile.user)
        execapp = ExecutiveAppointment.objects.filter(user=profile.user)
        retirement = Retirement.objects.filter(user=profile.user)

        context['govapp'] = get_object_or_404(
            GovernmentAppointment, user=profile.user)
        context['qualifications'] = qualifications
        context['pro_qualifications'] = pro_qualifications
        context['promotion'] = promotion
        context['discipline'] = discipline
        context['leave'] = leave
        context['execapp'] = execapp
        context['retirement'] = retirement
        context['Qualform'] = QualForm()
        context['ProQualform'] = ProQualForm()
        context['Promotionform'] = PromotionForm()
        context['Leaveform'] = LeaveForm()
        context['Disciplineform'] = DisciplineForm()
        context['Execappform'] = ExecappForm()
        context['Retireform'] = RetireForm()
        return context


@method_decorator(login_required(login_url='login'), name='dispatch')
class GovappDetailView(DetailView):
    template_name = 'staff//profile_details.html'
    model = Profile

    def get_object(self, queryset=None):
        if self.request.user.is_superuser:
            username_from_url = self.kwargs.get('username')
            user = get_object_or_404(User, username=username_from_url)
        else:
            user = self.request.user
        return get_object_or_404(Profile, user=user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = context['object']

        context['govapp'] = get_object_or_404(
            GovernmentAppointment, user=profile.user)
        return context


@method_decorator(login_required(login_url='login'), name='dispatch')
class QualCreateView(CreateView):
    model = Qualification
    form_class = QualForm
    template_name = 'staff/qual.html'

    def form_valid(self, form):
        if self.request.user.is_superuser:
            # If the current user is a superuser, use the username from the URL
            username_from_url = self.kwargs.get('username')
            user = get_object_or_404(User, username=username_from_url)
            form.instance.user = user
        else:
            # If the current user is not a superuser, use the current user
            form.instance.user = self.request.user

        return super().form_valid(form)

    def get_success_url(self):
        messages.success(self.request, 'Qualification Added Successfully')
        return reverse_lazy('profile_details', kwargs={'username': self.kwargs['username']})


@method_decorator(login_required(login_url='login'), name='dispatch')
class QualUpdateView(UpdateView):
    model = Qualification
    form_class = QualForm
    template_name = 'staff/qual-update.html'

    def get_success_url(self):
        messages.success(self.request, 'Qualification Updated Successfully')
        return reverse_lazy('profile_details', kwargs={'username': self.object.user.username})

    def form_invalid(self, form):
        messages.error(self.request, 'Error Updating Qualification')
        return super().form_invalid(form)


@method_decorator(login_required(login_url='login'), name='dispatch')
class QualDeleteView(DeleteView):
    model = Qualification
    template_name = 'staff/qual-delete-confirm.html'

    def get_success_url(self):
        messages.success(self.request, 'Qualification deleted successfully')
        return reverse_lazy('profile_details', kwargs={'username': self.object.user.username})

    def delete(self, request, *args, **kwargs):
        response = super().delete(request, *args, **kwargs)
        if response.status_code == 302:
            messages.success(
                self.request, 'Qualification deleted successfully')
        else:
            messages.error(self.request, 'Error deleting qualification')
        return response


@method_decorator(login_required(login_url='login'), name='dispatch')
class ProQualCreateView(CreateView):
    model = ProfessionalQualification
    form_class = ProQualForm
    template_name = 'staff/pro-qual.html'

    def form_valid(self, form):
        if self.request.user.is_superuser:
            # If the current user is a superuser, use the username from the URL
            username_from_url = self.kwargs.get('username')
            user = get_object_or_404(User, username=username_from_url)
            form.instance.user = user
        else:
            # If the current user is not a superuser, use the current user
            form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        messages.success(
            self.request, 'Professional Qualification Added Successfully')
        return reverse_lazy('profile_details', kwargs={'username': self.kwargs['username']})


@method_decorator(login_required(login_url='login'), name='dispatch')
class ProQualUpdateView(UpdateView):
    model = ProfessionalQualification
    form_class = ProQualForm
    template_name = 'staff/pro-qual-update.html'

    def get_success_url(self):
        messages.success(
            self.request, 'Professional Qualification Updated Successfully')
        return reverse_lazy('profile_details', kwargs={'username': self.object.user.username})

    def form_invalid(self, form):
        messages.error(
            self.request, 'Error Updating Professional Qualification')
        return super().form_invalid(form)


@method_decorator(login_required(login_url='login'), name='dispatch')
class ProQualDeleteView(DeleteView):
    model = ProfessionalQualification
    template_name = 'staff/pro-qual-delete-confirm.html'

    def get_success_url(self):
        messages.success(
            self.request, 'Professional Qualification deleted successfully')
        return reverse_lazy('profile_details', kwargs={'username': self.object.user.username})

    def delete(self, request, *args, **kwargs):
        response = super().delete(request, *args, **kwargs)
        if response.status_code == 302:
            messages.success(
                self.request, 'Professional Qualification deleted successfully')
        else:
            messages.error(
                self.request, 'Error deleting professional qualification')
        return response


@method_decorator(login_required(login_url='login'), name='dispatch')
class PromotionCreateView(CreateView):
    model = Promotion
    form_class = PromotionForm
    template_name = 'staff/promotion.html'

    def form_valid(self, form):
        if self.request.user.is_superuser:
            # If the current user is a superuser, use the username from the URL
            username_from_url = self.kwargs.get('username')
            user = get_object_or_404(User, username=username_from_url)
            form.instance.user = user
        else:
            # If the current user is not a superuser, use the current user
            form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        messages.success(self.request, 'Promotion Added Successfully')
        return reverse_lazy('profile_details', kwargs={'username': self.kwargs['username']})


@method_decorator(login_required(login_url='login'), name='dispatch')
class PromotionUpdateView(UpdateView):
    model = Promotion
    form_class = PromotionForm
    template_name = 'staff/promotion-update.html'

    def get_success_url(self):
        messages.success(self.request, 'Promotion Updated Successfully')
        return reverse_lazy('profile_details', kwargs={'username': self.object.user.username})

    def form_invalid(self, form):
        messages.error(self.request, 'Error Updating Promotion')
        return super().form_invalid(form)


@method_decorator(login_required(login_url='login'), name='dispatch')
class PromotionDeleteView(DeleteView):
    model = Promotion
    template_name = 'staff/promotion-delete-confirm.html'

    def get_success_url(self):
        messages.success(self.request, 'Promotion deleted successfully')
        return reverse_lazy('profile_details', kwargs={'username': self.object.user.username})

    def delete(self, request, *args, **kwargs):
        response = super().delete(request, *args, **kwargs)
        if response.status_code == 302:
            messages.success(self.request, 'Promotion deleted successfully')
        else:
            messages.error(self.request, 'Error deleting promotion')
        return response


@method_decorator(login_required(login_url='login'), name='dispatch')
class DisciplineCreateView(CreateView):
    model = Discipline
    form_class = DisciplineForm
    template_name = 'staff/discipline.html'

    def form_valid(self, form):
        if self.request.user.is_superuser:
            # If the current user is a superuser, use the username from the URL
            username_from_url = self.kwargs.get('username')
            user = get_object_or_404(User, username=username_from_url)
            form.instance.user = user
        else:
            # If the current user is not a superuser, use the current user
            form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        messages.success(self.request, 'Discipline Added Successfully')
        return reverse_lazy('profile_details', kwargs={'username': self.kwargs['username']})

    def form_invalid(self, form):
        messages.error(self.request, 'Error Adding Discipline')
        return super().form_invalid(form)

@method_decorator(login_required(login_url='login'), name='dispatch')
class DisciplineUpdateView(UpdateView):
    model = Discipline
    form_class = DisciplineForm
    template_name = 'staff/discipline-update.html'

    def get_success_url(self):
        messages.success(self.request, 'Discipline Updated Successfully')
        return reverse_lazy('profile_details', kwargs={'username': self.object.user.username})

    def form_invalid(self, form):
        messages.error(self.request, 'Error Updating Discipline')
        return super().form_invalid(form)


@method_decorator(login_required(login_url='login'), name='dispatch')
class DisciplineDeleteView(DeleteView):
    model = Discipline
    template_name = 'staff/discipline-delete-confirm.html'

    def get_success_url(self):
        messages.success(self.request, 'Discipline deleted successfully')
        return reverse_lazy('profile_details', kwargs={'username': self.object.user.username})

    def delete(self, request, *args, **kwargs):
        response = super().delete(request, *args, **kwargs)
        if response.status_code == 302:
            messages.success(self.request, 'Discipline deleted successfully')
        else:
            messages.error(self.request, 'Error deleting discipline')
        return response


@method_decorator(login_required(login_url='login'), name='dispatch')
class LeaveCreateView(CreateView):
    model = Leave
    form_class = LeaveForm
    template_name = 'staff/leave.html'

    def form_valid(self, form):
        if self.request.user.is_superuser:
            # If the current user is a superuser, use the username from the URL
            username_from_url = self.kwargs.get('username')
            user = get_object_or_404(User, username=username_from_url)
            form.instance.user = user
        else:
            # If the current user is not a superuser, use the current user
            form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        messages.success(self.request, 'Leave Added Successfully')
        return reverse_lazy('profile_details', kwargs={'username': self.kwargs['username']})


@method_decorator(login_required(login_url='login'), name='dispatch')
class LeaveUpdateView(UpdateView):
    model = Leave
    form_class = LeaveForm
    template_name = 'staff/leave-update.html'

    def get_success_url(self):
        messages.success(self.request, 'Leave Updated Successfully')
        return reverse_lazy('profile_details', kwargs={'username': self.object.user.username})

    def form_invalid(self, form):
        messages.error(self.request, 'Error Updating Leave')
        return super().form_invalid(form)


@method_decorator(login_required(login_url='login'), name='dispatch')
class LeaveDeleteView(DeleteView):
    model = Leave
    template_name = 'staff/leave-delete-confirm.html'

    def get_success_url(self):
        messages.success(self.request, 'Leave deleted successfully')
        return reverse_lazy('profile_details', kwargs={'username': self.object.user.username})

    def delete(self, request, *args, **kwargs):
        response = super().delete(request, *args, **kwargs)
        if response.status_code == 302:
            messages.success(self.request, 'Leave deleted successfully')
        else:
            messages.error(self.request, 'Error deleting leave')
        return response


@method_decorator(login_required(login_url='login'), name='dispatch')
class ExecappCreateView(CreateView):
    model = ExecutiveAppointment
    form_class = ExecappForm
    template_name = 'staff/execapp.html'

    def form_valid(self, form):
        if self.request.user.is_superuser:
            # If the current user is a superuser, use the username from the URL
            username_from_url = self.kwargs.get('username')
            user = get_object_or_404(User, username=username_from_url)
            form.instance.user = user
        else:
            # If the current user is not a superuser, use the current user
            form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        messages.success(
            self.request, 'Executive Appointment Added Successfully')
        return reverse_lazy('profile_details', kwargs={'username': self.kwargs['username']})


@method_decorator(login_required(login_url='login'), name='dispatch')
class ExecappUpdateView(UpdateView):
    model = ExecutiveAppointment
    form_class = ExecappForm
    template_name = 'staff/execapp-update.html'

    def get_success_url(self):
        messages.success(
            self.request, 'Executive Appointment Updated Successfully')
        return reverse_lazy('profile_details', kwargs={'username': self.object.user.username})

    def form_invalid(self, form):
        messages.error(self.request, 'Error Updating Executive Appointment')
        return super().form_invalid(form)


@method_decorator(login_required(login_url='login'), name='dispatch')
class ExecappDeleteView(DeleteView):
    model = ExecutiveAppointment
    template_name = 'staff/execapp-delete-confirm.html'

    def get_success_url(self):
        messages.success(
            self.request, 'Executive Appointment deleted successfully')
        return reverse_lazy('profile_details', kwargs={'username': self.object.user.username})

    def delete(self, request, *args, **kwargs):
        response = super().delete(request, *args, **kwargs)
        if response.status_code == 302:
            messages.success(
                self.request, 'Executive Appointment deleted successfully')
        else:
            messages.error(
                self.request, 'Error deleting executive appointment')
        return response


@method_decorator(login_required(login_url='login'), name='dispatch')
class RetireCreateView(CreateView):
    model = Retirement
    form_class = RetireForm
    template_name = 'staff/retire.html'

    def form_valid(self, form):
        if self.request.user.is_superuser:
            # If the current user is a superuser, use the username from the URL
            username_from_url = self.kwargs.get('username')
            user = get_object_or_404(User, username=username_from_url)
            form.instance.user = user
            
            
        else:
            # If the current user is not a superuser, use the current user
            form.instance.user = self.request.user
            
        return super().form_valid(form)

    def get_success_url(self):
        messages.success(self.request, 'Retirement Added Successfully')
        return reverse_lazy('profile_details', kwargs={'username': self.kwargs['username']})


@method_decorator(login_required(login_url='login'), name='dispatch')
class RetireUpdateView(UpdateView):
    model = Retirement
    form_class = RetireForm
    template_name = 'staff/retire-update.html'

    def get_success_url(self):
        messages.success(self.request, 'Retirement Updated Successfully')
        return reverse_lazy('profile_details', kwargs={'username': self.object.user.username})

    def form_invalid(self, form):
        messages.error(self.request, 'Error Updating Retirement')
        return super().form_invalid(form)


@method_decorator(login_required(login_url='login'), name='dispatch')
class RetireDeleteView(DeleteView):
    model = Retirement
    template_name = 'staff/retire-delete-confirm.html'

    def get_success_url(self):
        messages.success(self.request, 'Retire deleted successfully')
        return reverse_lazy('profile_details', kwargs={'username': self.object.user.username})

    def delete(self, request, *args, **kwargs):
        response = super().delete(request, *args, **kwargs)
        if response.status_code == 302:
            messages.success(self.request, 'Retire deleted successfully')
        else:
            messages.error(self.request, 'Error deleting retirement')
        return response
