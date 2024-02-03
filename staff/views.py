from django.shortcuts import render,get_object_or_404,HttpResponseRedirect
from django.views.generic.edit import UpdateView, CreateView, DeleteView
from django.views.generic import DetailView, ListView
from django.views import View
from .forms import CustomUserCreationForm
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.views import LoginView, LogoutView
from .models import *
from .forms import *
from .filters import *
from django.contrib.auth import get_user_model
User = get_user_model()


def log_anonymous_required(view_function, redirect_to=None):
    if redirect_to is None:
        redirect_to = '/'
    return user_passes_test(lambda u: not u.is_authenticated,login_url=redirect_to)(view_function)


def index(request):
    return render(request, 'index.html')

def manage(request):
    return render(request, 'manage.html')

def staff(request):
    p=Profile.objects.all()
    context={'p':p}
    return render(request, 'staff/stafflist.html',context)

def dept(request):
    return render(request, 'dept.html')

def dept_details(request):
    pass

def dirs(request):
    return render(request, 'dirs.html')

def dirs_details(request):
    pass

def report(request):
    return render(request, 'report.html')


class GenReportView(ListView):
    model = get_user_model()
    template_name = 'staff/gen_report.html'
    paginate_by = 10
    context_object_name = 'users'

    def get_queryset(self):
        queryset = super().get_queryset()
        total = queryset.filter(is_active=True, is_superuser=False).count()

        gen_filter = GovFilter(self.request.GET, queryset=queryset)
        users = gen_filter.qs.order_by('governmentappointment__department')

        self.total = total
        return users

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['gen_filter'] = GovFilter(self.request.GET, queryset=self.get_queryset())
        context['total'] = self.total
        return context


def pro_report(request):
    pass
    # return render(request, 'pro_report.html')

def govapp_report(request):
    pass
    # return render(request, 'govapp_report.html')

def lv_report(request):
    pass
    # return render(request, 'lv_report.html')

def dis_report(request):
    pass
    # return render(request, 'dis_report.html')

def qual_report(request):
    pass
    # return render(request, 'qual_report.html')

def pro_qual_report(request):
    pass
    # return render(request, 'pro_qual_report.html')

def rt_report(request):
    pass
    # return render(request, 'rt_report.html')

def stats(request):
    return render(request, 'stats.html')

def notice(request):
    return render(request, 'notice.html')


@method_decorator(log_anonymous_required, name='dispatch')
class CustomLoginView(LoginView):
    template_name='login.html'
    def get_success_url(self):
        if self.request.user.is_superuser:
            return reverse_lazy('index')
        else:
            return reverse_lazy('profile_details',args=[self.request.user.username])


@method_decorator(login_required, name='dispatch')
class CustomLogoutView(LogoutView):
    template_name='logged_out.html'


def reg_anonymous_required(view_function, redirect_to=None):
    if redirect_to is None:
        redirect_to = '/'
    return user_passes_test(lambda u: not u.is_authenticated or u.is_superuser,login_url=redirect_to)(view_function)


@method_decorator(reg_anonymous_required, name='dispatch')
class UserRegistrationView(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        if form.is_valid():
            response = super().form_valid(form)
            user = User.objects.get(username=form.cleaned_data['username'])
            profile_instance = Profile(user=user)
            profile_instance.save()
            govapp_instance = GovernmentAppointment(user=user)
            govapp_instance.save()
            messages.success(self.request, f"Registration for: {user.get_full_name()} was successful")
            return response
        else:
            print("Form errors:", form.errors)
            return self.form_invalid(form)
        

class DocumentationView(UpdateView):
    model = User
    template_name = 'doc.html'
    form_class = UserForm
    success_url = reverse_lazy('index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profileform'] = ProfileForm(instance=self.object.profile)
        context['govtappform'] = GovtAppForm(instance=self.object.governmentappointment)
        return context

    def form_valid(self, form):
        userform=UserForm(self.request.POST, instance=self.object)
        profileform = ProfileForm(self.request.POST, instance=self.object.profile)
        govtappform = GovtAppForm(self.request.POST, instance=self.object.governmentappointment)

        if userform.is_valid() and profileform.is_valid() and govtappform.is_valid():
            userform.save()
            profileform.save()
            govtappform.save()
            messages.success(self.request, f'Documentation successful for:{self.request.user.last_name}')
            return HttpResponseRedirect(self.get_success_url())
        else:
            messages.error(self.request, 'Please correct the errors to proceed')
            return self.form_invalid(form)


@method_decorator(login_required(login_url='login'), name='dispatch')
class UpdateUserView(UpdateView):
    model=User
    template_name= 'staff/update-user.html'
    form_class=UserForm
    success_url=reverse_lazy('profile_details')

    def get_success_url(self):
        messages.success(self.request, 'Staff Information Updated Successfully')
        return reverse_lazy('profile_details', kwargs={'username': self.object.username})

    def form_valid(self,form):
        if form.is_valid():
            form.save()
            return super().form_valid(form)
        else:
            return self.form_invalid(form)

    def form_invalid(self,form):
        messages.error(self.request,'error updating staff information')
        return self.render_to_response(self.get_context_data(form=form))


@method_decorator(login_required(login_url='login'), name='dispatch')
class UpdateProfileView(UpdateView):
    model=Profile
    template_name = 'staff/update-profile.html'
    form_class=ProfileForm
    success_url=reverse_lazy('profile_details')

    def get_success_url(self):
        messages.success(self.request, 'Staff Information Updated Successfully')
        return reverse_lazy('profile_details', kwargs={'username': self.object.user})

    def form_valid(self,form):
        if form.is_valid():
            form.save()
            return super().form_valid(form)
        else:
            return self.form_invalid(form)

    def form_invalid(self,form):
        messages.error(self.request,'error updating staff information')
        return self.render_to_response(self.get_context_data(form=form))


@method_decorator(login_required(login_url='login'), name='dispatch')
class UpdateGovappView(UpdateView):
    model=GovernmentAppointment
    template_name = 'staff/update-govapp.html'
    form_class=GovtAppForm
    success_url=reverse_lazy('profile_details')

    def get_success_url(self):
        messages.success(self.request, 'Staff Information Updated Successfully')
        return reverse_lazy('profile_details', kwargs={'username': self.object.user})

    def form_invalid(self,form):
        messages.error(self.request,'error updating staff information')
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
        pro_qualifications = ProfessionalQualification.objects.filter(user=profile.user)
        promotion = Promotion.objects.filter(user=profile.user)
        discipline = Discipline.objects.filter(user=profile.user)
        leave = Leave.objects.filter(user=profile.user)
        execapp = ExecutiveAppointment.objects.filter(user=profile.user)
        retirement = Retirement.objects.filter(user=profile.user)

        context['govapp'] = get_object_or_404(GovernmentAppointment, user=profile.user)
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
    model=Qualification
    form_class=QualForm
    template_name='staff/qual-update.html'

    def get_success_url(self):
        messages.success(self.request, 'Qualification Updated Successfully')
        return reverse_lazy('profile_details', kwargs={'username': self.object.user.username})
    
    def form_invalid(self,form):
        messages.error(self.request,'Error Updating Qualification')
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
            messages.success(self.request, 'Qualification deleted successfully')
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
        messages.success(self.request, 'Professional Qualification Added Successfully')
        return reverse_lazy('profile_details', kwargs={'username': self.kwargs['username']})


@method_decorator(login_required(login_url='login'), name='dispatch')
class ProQualUpdateView(UpdateView):
    model=ProfessionalQualification
    form_class=ProQualForm
    template_name='staff/pro-qual-update.html'

    def get_success_url(self):
        messages.success(self.request, 'Professional Qualification Updated Successfully')
        return reverse_lazy('profile_details', kwargs={'username': self.object.user.username})
    
    def form_invalid(self,form):
        messages.error(self.request,'Error Updating Professional Qualification')
        return super().form_invalid(form)
    

@method_decorator(login_required(login_url='login'), name='dispatch')
class ProQualDeleteView(DeleteView):
    model = ProfessionalQualification
    template_name = 'staff/pro-qual-delete-confirm.html'

    def get_success_url(self):
        messages.success(self.request, 'Professional Qualification deleted successfully')
        return reverse_lazy('profile_details', kwargs={'username': self.object.user.username})

    def delete(self, request, *args, **kwargs):
        response = super().delete(request, *args, **kwargs)
        if response.status_code == 302:
            messages.success(self.request, 'Professional Qualification deleted successfully')
        else:
            messages.error(self.request, 'Error deleting professional qualification')
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
    model=Promotion
    form_class=PromotionForm
    template_name='staff/promotion-update.html'

    def get_success_url(self):
        messages.success(self.request, 'Promotion Updated Successfully')
        return reverse_lazy('profile_details', kwargs={'username': self.object.user.username})
    
    def form_invalid(self,form):
        messages.error(self.request,'Error Updating Promotion')
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


@method_decorator(login_required(login_url='login'), name='dispatch')
class DisciplineUpdateView(UpdateView):
    model=Discipline
    form_class=DisciplineForm
    template_name='staff/discipline-update.html'

    def get_success_url(self):
        messages.success(self.request, 'Discipline Updated Successfully')
        return reverse_lazy('profile_details', kwargs={'username': self.object.user.username})
    
    def form_invalid(self,form):
        messages.error(self.request,'Error Updating Discipline')
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
    model=Leave
    form_class=LeaveForm
    template_name='staff/leave-update.html'

    def get_success_url(self):
        messages.success(self.request, 'Leave Updated Successfully')
        return reverse_lazy('profile_details', kwargs={'username': self.object.user.username})
    
    def form_invalid(self,form):
        messages.error(self.request,'Error Updating Leave')
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
        messages.success(self.request, 'Executive Appointment Added Successfully')
        return reverse_lazy('profile_details', kwargs={'username': self.kwargs['username']})


@method_decorator(login_required(login_url='login'), name='dispatch')
class ExecappUpdateView(UpdateView):
    model=ExecutiveAppointment
    form_class=ExecappForm
    template_name='staff/execapp-update.html'

    def get_success_url(self):
        messages.success(self.request, 'Executive Appointment Updated Successfully')
        return reverse_lazy('profile_details', kwargs={'username': self.object.user.username})
    
    def form_invalid(self,form):
        messages.error(self.request,'Error Updating Executive Appointment')
        return super().form_invalid(form)
    

@method_decorator(login_required(login_url='login'), name='dispatch')
class ExecappDeleteView(DeleteView):
    model = ExecutiveAppointment
    template_name = 'staff/execapp-delete-confirm.html'

    def get_success_url(self):
        messages.success(self.request, 'Executive Appointment deleted successfully')
        return reverse_lazy('profile_details', kwargs={'username': self.object.user.username})

    def delete(self, request, *args, **kwargs):
        response = super().delete(request, *args, **kwargs)
        if response.status_code == 302:
            messages.success(self.request, 'Executive Appointment deleted successfully')
        else:
            messages.error(self.request, 'Error deleting executive appointment')
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
    model=Retirement
    form_class=RetireForm
    template_name='staff/retire-update.html'

    def get_success_url(self):
        messages.success(self.request, 'Retirement Updated Successfully')
        return reverse_lazy('profile_details', kwargs={'username': self.object.user.username})
    
    def form_invalid(self,form):
        messages.error(self.request,'Error Updating Retirement')
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
