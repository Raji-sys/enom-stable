from django.shortcuts import render,get_object_or_404,HttpResponseRedirect
from django.views.generic.edit import UpdateView, CreateView, DeleteView
from django.views.generic import DetailView
from .forms import CustomUserCreationForm
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.views import LoginView, LogoutView
from .models import *
from .forms import *
from django.contrib.auth import get_user_model
from django.views import View
from django.http import Http404
User = get_user_model()


def log_anonymous_required(view_function, redirect_to=None):
    if redirect_to is None:
        redirect_to = '/'
    return user_passes_test(lambda u: not u.is_authenticated,login_url=redirect_to)(view_function)


def index(request):
    p=Profile.objects.all()
    context={'p':p}
    return render(request, 'index.html',context)


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
            messages.success(self.request, f"Registration for {user.get_full_name()} was successful")
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
            messages.success(self.request, f'Documentation was successful {self.request.user.last_name}')
            return HttpResponseRedirect(self.get_success_url())
        else:
            messages.error(self.request, 'Please correct the errors')
            return self.form_invalid(form)


@method_decorator(login_required(login_url='login'), name='dispatch')
class UpdateUserView(UpdateView):
    model=User
    template_name= 'staff/update-user.html'
    form_class=UserForm
    success_url=reverse_lazy('profile_details')

    def get_success_url(self):
        return reverse_lazy('profile_details', kwargs={'username': self.object.username})

    def form_valid(self,form):
        if form.is_valid():
            form.save()
            messages.success(self.request, 'User Information Updated Successfully')
            return super().form_valid(form)
        else:
            return self.form_invalid(form)

    def form_invalid(self,form):
        messages.error(self.request,'Please Correct the error')
        return self.render_to_response(self.get_context_data(form=form))


@method_decorator(login_required(login_url='login'), name='dispatch')
class UpdateProfileView(UpdateView):
    model=Profile
    template_name = 'staff/update-profile.html'
    form_class=ProfileForm
    success_url=reverse_lazy('profile_details')

    def get_success_url(self):
        return reverse_lazy('profile_details', kwargs={'username': self.object.user})

    def form_valid(self,form):
        if form.is_valid():
            form.save()
            messages.success(self.request, 'User Information Updated Successfully')
            return super().form_valid(form)
        else:
            return self.form_invalid(form)

    def form_invalid(self,form):
        messages.error(self.request,'Please Correct the error')
        return self.render_to_response(self.get_context_data(form=form))


# @method_decorator(login_required(login_url='login'), name='dispatch')
# class UpdateGovappView(UpdateView):
#     model=GovernmentAppointment
#     template_name = 'staff/update-govapp.html'
#     form_class=GovtAppForm
#     success_url=reverse_lazy('profile_details')

#     def get_success_url(self):
#         return reverse_lazy('profile_details', kwargs={'username': self.object.user})

#     def form_valid(self,form):
#         if form.is_valid():
#             form.save()
#             messages.success(self.request, 'User Information Updated Successfully')
#             return super().form_valid(form)
#         else:
#             return self.form_invalid(form)

#     def form_invalid(self,form):
#         messages.error(self.request,'Please Correct the error')
#         return self.render_to_response(self.get_context_data(form=form))


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

        # Retrieve qualifications associated with the user
        qualifications = Qualification.objects.filter(user=profile.user)

        context['govapp'] = get_object_or_404(GovernmentAppointment, user=profile.user)
        context['qualifications'] = qualifications
        context['Qualform'] = QualForm()
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
        return reverse_lazy('profile_details', kwargs={'username': self.kwargs['username']})


# @method_decorator(login_required(login_url='login'), name='dispatch')
# class QualUpdateView(UpdateView):
#     model=Qualification
#     form_class=QualForm
#     template_name='staff/qual-update.html'

#     def get_success_url(self):
#         messages.success(self.request, 'Qualification Updated Successfully')
#         return reverse_lazy('profile_details', kwargs={'username': self.object.user.username})
    
#     def form_invalid(self,form):
#         messages.error(self.request,'Error Updating Qualification')
#         return super().form_invalid(form)
    

# @method_decorator(login_required(login_url='login'), name='dispatch')
# class QualDeleteView(DeleteView):
#     model=Qualification
#     template_name='staff/qual-delete-confirm.html'

#     def get_success_url(self):
#         messages.success(self.request, 'Qualification Deleted Successfully')
#         return reverse_lazy('profile_details', kwargs={'username': self.object.user.username})



class UpdateProfileMixin:
    success_message = ''

    def form_valid(self, form):
        messages.success(self.request, self.success_message)
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Please correct the error.')
        return self.render_to_response(self.get_context_data(form=form))

class UpdateGovappView(UpdateProfileMixin, UpdateView):
    model = GovernmentAppointment
    template_name = 'staff/update-govapp.html'
    form_class = GovtAppForm
    success_url = reverse_lazy('profile_details')
    success_message = 'User Information Updated Successfully'

class QualUpdateView(UpdateProfileMixin, UpdateView):
    model = Qualification
    template_name = 'staff/qual-update.html'
    form_class = QualForm
    success_url = reverse_lazy('profile_details')
    success_message = 'Qualification updated successfully.'

class QualDeleteView(DeleteView):
    model = Qualification
    template_name = 'staff/qual-delete-confirm.html'

    def get_success_url(self):
        messages.success(self.request, 'Qualification deleted successfully.')
        return reverse_lazy('profile_details', kwargs={'username': self.object.user.username})

    def delete(self, request, *args, **kwargs):
        response = super().delete(request, *args, **kwargs)
        if response.status_code == 302:
            messages.success(self.request, 'Qualification deleted successfully.')
        else:
            messages.error(self.request, 'Error deleting qualification.')
        return response
