from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.views.generic.edit import CreateView
from .forms import CustomUserCreationForm
from django.contrib import messages
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.paginator import Paginator
from django.contrib.auth.views import LoginView
from .models import *
from .forms import *
from django.contrib.auth import get_user_model
User = get_user_model()  # Get the User model

def log_anonymous_required(view_function, redirect_to=None):
    """
    Decorator for views that checks if the user is not logged in.
    """
    if redirect_to is None:
        redirect_to = '/'

    return user_passes_test(
        lambda u: not u.is_authenticated,
        login_url=redirect_to
    )(view_function)


@login_required
def index(request):
    return render(request, 'index.html')

@method_decorator(log_anonymous_required, name='dispatch')
class CustomLoginView(LoginView):
    template_name='login.html'
    success_url=reverse_lazy('/')


def reg_anonymous_required(view_function, redirect_to=None):
    """
    Decorator for views that checks if the user is not registered or is a superuser.
    """
    if redirect_to is None:
        redirect_to = '/'

    return user_passes_test(
        lambda u: not u.is_authenticated or u.is_superuser,
        login_url=redirect_to
    )(view_function)


@method_decorator(reg_anonymous_required, name='dispatch')
class UserRegistrationView(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        if form.is_valid():
            response = super().form_valid(form)
            
            # Ensure the user is created
            user = User.objects.get(username=form.cleaned_data['username'])

            # Create the profile
            profile_instance = Profile(user=user)
            profile_instance.save()

            # Create the government appointment
            govapp_instance = GovernmentAppointment(user=user)
            govapp_instance.save()

            return response
        else:
            print("Form errors:", form.errors)
            return self.form_invalid(form)
        

class DocumentationView(CreateView):
    model = Profile
    form_class = ProfileForm
    template_name = 'doc.html'
    success_url = reverse('user')

    def get(self, request, *args, **kwargs):
        user_profile = self.request.user.profile

        # Check if staff_no is empty
        if user_profile.staff_no is None:
            govtappform = GovtAppForm(instance=self.request.user.governmentappointment)
            profileform = ProfileForm(instance=user_profile)

            context = {'profileform': profileform, 'govtappform': govtappform}

            return render(request, self.template_name, context)
        else:
            return HttpResponseRedirect(self.success_url)

    def post(self, request, *args, **kwargs):
        profileform = ProfileForm(request.POST, instance=request.user.profile)
        govtappform = GovtAppForm(request.POST, instance=request.user.governmentappointment)

        if profileform.is_valid() and govtappform.is_valid():
            profileform.save()
            govtappform.save()
            messages.success(request, 'Documentation was successful {}'.format(request.user.get_full_name()))
            return HttpResponseRedirect(self.success_url)
        else:
            messages.error(request, 'Please correct the errors')
            return self.form_invalid(profileform)