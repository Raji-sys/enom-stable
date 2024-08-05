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
from django.db.models import Sum, Count
from django.db.models import Q
from django.http import JsonResponse
User = get_user_model()
from django.db.models import Prefetch
from django.db import transaction



def log_anonymous_required(view_function, redirect_to=None):
    if redirect_to is None:
        redirect_to = '/'
    return user_passes_test(lambda u: not u.is_authenticated, login_url=redirect_to)(view_function)


@login_required
def fetch_resources(uri, rel):
    if uri.startswith(settings.STATIC_URL):
        path = os.path.join(settings.STATIC_ROOT,uri.replace(settings.STATIC_URL, ""))
    else:
        path = os.path.join(settings.MEDIA_ROOT,uri.replace(settings.MEDIA_URL, ""))
    return path


@method_decorator(login_required(login_url='login'), name='dispatch')
class IndexView(TemplateView):
    template_name = "index.html"


@method_decorator(login_required(login_url='login'), name='dispatch')
class StaffListView(ListView):
    model = Profile
    template_name = "staff/stafflist.html"
    context_object_name = 'profiles'
    paginate_by = 10

    def get_queryset(self):
        queryset = Profile.objects.all()
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(
                Q(user__first_name__icontains=query) |
                Q(user__last_name__icontains=query) |
                Q(middle_name__icontains=query) |
                Q(file_no__icontains=query) |
                Q(user__govapp__department__name__icontains=query)
            )
        return queryset.order_by('user__govapp__department__name')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        total_profiles = self.get_queryset().count()
        context['total_profiles'] = total_profiles
        context['query'] = self.request.GET.get('q', '')
        return context


@method_decorator(login_required(login_url='login'), name='dispatch')
class DepartmmentList(ListView):
    model=Department
    template_name='dept.html'
    context_object_name='departments'

    
@method_decorator(login_required(login_url='login'), name='dispatch')
class DepartmentDetail(DetailView):
    model=Department
    template_name='dept_details.html'


@method_decorator(login_required(login_url='login'), name='dispatch')
class PostList(ListView):
    model=Post
    template_name='post.html'
    context_object_name='posts'


@method_decorator(login_required(login_url='login'), name='dispatch')
class PostDetail(DetailView):
    model=Post
    template_name='post_details.html'


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
        sc_counts = Qualification.objects.values('school_department').annotate(pc=Count('id'))
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
class NoticePromotionView(TemplateView):
    template_name ="notice_promotion.html"
    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        due_appts=GovernmentAppointment.objects.filter(due=True).select_related('user__profile')
        context.update({
            'due_count':due_appts.count(),
            'due_appts':due_appts,
        })
        return context


@method_decorator(login_required(login_url='login'), name='dispatch')
class NoticeLeaveView(TemplateView):
    template_name="notice_leave.html"
    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        leave_st=Leave.objects.filter(is_leave_over=True).select_related('user__profile')
        context.update({
            'leave_count':leave_st.count(),
            'leave_st':leave_st,
        })
        return context

@method_decorator(login_required(login_url='login'), name='dispatch')
class NoticeRetirementView(TemplateView):
    template_name="notice_retire.html"
    
    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        retire_st= GovernmentAppointment.objects.filter(retire=True).select_related('user__profile') 
        context.update({
            'retire_count':retire_st.count(),
            'retire_st':retire_st,
        })
        return context


@method_decorator(login_required(login_url='login'), name='dispatch')
class NoticeView(TemplateView):
    template_name='notice.html'


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
                self.request, f"Registration successful: {user.get_full_name()} can now login")
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
        context['govtappform'] = GovtAppForm(instance=self.object.govapp)
        return context

    def form_valid(self, form):
        userform = UserForm(self.request.POST, instance=self.object)
        profileform = ProfileForm(self.request.POST, instance=self.object.profile)
        govtappform = GovtAppForm(self.request.POST, instance=self.object.govapp)

        if userform.is_valid() and profileform.is_valid() and govtappform.is_valid():
            userform.save()
            profileform.save()
            govtappform.save()
            messages.success(self.request, f'Documentation successful!{self.request.user.last_name}')
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


def get_states_by_zone(request, zone_id):
    states = State.objects.filter(zone_id=zone_id)
    state_list = [{'id': state.id, 'name': state.name} for state in states]
    return JsonResponse({'states': state_list})

def get_lgas_by_state(request, state_id):
    lgas = LGA.objects.filter(state_id=state_id)
    lga_list = [{'id': lga.id, 'name': lga.name} for lga in lgas]
    return JsonResponse({'lgas': lga_list})

def get_senate_districts_by_lga(request, lga_id):
    senate_districts = SenateDistrict.objects.filter(lga_id=lga_id)
    senate_district_list = [{'id': sd.id, 'name': sd.name} for sd in senate_districts]
    return JsonResponse({'senate_districts': senate_district_list})

def get_post_by_department(request, department_id):
    posts = Post.objects.filter(department_id=department_id)
    post_list = [{'id': post.id, 'name': post.name} for post in posts]
    return JsonResponse({'posts': post_list})


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
            username = self.kwargs.get('username')
            user = get_object_or_404(User, username=username)
        else:
            user = self.request.user
        return get_object_or_404(Profile.objects.select_related('user'), user=user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = context['object']
        user = profile.user

        related_models = [
            ('qualifications', Qualification),
            ('pro_qualifications', ProfessionalQualification),
            ('promotion', Promotion),
            ('discipline', Discipline),
            ('leave', Leave),
            ('execapp', ExecutiveAppointment),
            ('retirement', Retirement),
        ]

        for context_key, model in related_models:
            context[context_key] = model.objects.filter(user=user)

        context['govapp'] = get_object_or_404(GovernmentAppointment, user=user)

        form_classes = {
            'Qualform': QualForm,
            'ProQualform': ProQualForm,
            'Promotionform': PromotionForm,
            'Leaveform': LeaveForm,
            'Disciplineform': DisciplineForm,
            'Execappform': ExecappForm,
            'Retireform': RetireForm,
        }

        context.update({form_name: form_class() for form_name, form_class in form_classes.items()})
 # Add leave status to the context
        current_leave = Leave.objects.filter(user=user, year=timezone.now().year).last()
        context['leave_status'] = current_leave.leave_status if current_leave else "No leave taken this year."

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

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        if self.request.user.is_superuser:
            username_from_url = self.kwargs.get('username')
            user = get_object_or_404(User, username=username_from_url)
        else:
            user = self.request.user
        
        form.instance.user = user
        
        try:
            instance = form.save(commit=False)
            
            existing_leaves = Leave.objects.filter(
                user=user,
                year=instance.year,
                nature_of_leave=instance.nature_of_leave
            )
            
            if existing_leaves.exists():
                last_leave = existing_leaves.latest('created')
                instance.balance = last_leave.remain
                instance.total_days = last_leave.remain
            else:
                instance.balance = instance.total_days
            
            instance.save()
            
            messages.success(self.request, 'Leave Added Successfully')
            return super().form_valid(form)
        except ValidationError as e:
            for error in e.messages:
                form.add_error(None, error)
            return self.form_invalid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Error Adding Leave. Please check the form for errors.')
        return super().form_invalid(form)

    def get_success_url(self):
        return reverse_lazy('profile_details', kwargs={'username': self.kwargs['username']})


@method_decorator(login_required(login_url='login'), name='dispatch')
class LeaveUpdateView(UpdateView):
    model = Leave
    form_class = LeaveForm
    template_name = 'staff/leave-update.html'

    def form_valid(self, form):
        try:
            return super().form_valid(form)
        except ValidationError as e:
            for field, errors in e.message_dict.items():
                for error in errors:
                    form.add_error(field, error)
            return self.form_invalid(form)

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
