from django.shortcuts import render,get_object_or_404,HttpResponseRedirect
from django.views.generic.edit import UpdateView, CreateView
from .forms import CustomUserCreationForm
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.paginator import Paginator
from django.contrib.auth.views import LoginView
from .models import *
from .forms import *
from django.contrib.auth import get_user_model
from django.views import View
User = get_user_model()


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


# @login_required
def index(request):
    p=Profile.objects.all()
    context={'p':p}
    return render(request, 'index.html',context)

@method_decorator(log_anonymous_required, name='dispatch')
class CustomLoginView(LoginView):
    template_name='login.html'
    # success_url=reverse_lazy('/')

    def get_success_url(self):
        return reverse_lazy('profile_details',args=[self.request.user.username])

    # def form_valid(self,form):
    #     response=super().form_valid(form)
    #     messages.success(self.request, f"welcome back, {self.request.user.get_full_name()}!")

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
class ProfileDetailView(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_superuser:
            # If the user is a superuser, retrieve the profile based on the username in the URL
            username_from_url = kwargs.get('username')  # Assuming you pass the username in the URL
            profile = get_object_or_404(Profile, user__username=username_from_url)
            govapp = get_object_or_404(GovernmentAppointment, user__username=username_from_url)
            # promotion = get_object_or_404(Promotion, user__username=username_from_url)
        else:
            # If the user is not a superuser, display the profile of the logged-in user
            profile = request.user.profile
            govapp = get_object_or_404(GovernmentAppointment, user=request.user)
            # promotion = get_object_or_404(Promotion, user=request.user)

        context = {
            'profile': profile,
            'govapp': govapp,
            # 'promotion': promotion,
        }
        return render(request, 'staff/profile_details.html', context)