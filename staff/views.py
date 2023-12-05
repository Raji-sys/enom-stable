from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.views.generic.edit import CreateView
from .forms import CustomUserCreationForm
from django.contrib import messages
from django.urls import reverse
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.paginator import Paginator
from django.contrib.auth.views import LoginView
from .models import *


@login_required
def index(request):
    return render(request, 'index.html')

def user_is_in(user):
    return not user.is_authenticated


# @method_decorator(user_passes_test(user_is_in, login_url='/'), name='dispatch')
class CustomLoginView(LoginView):
    template_name='login.html'
    success_url=reverse_lazy('/')


class UserRegistrationView(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('login')  # Redirect to login page upon successful registration

    def form_valid(self, form):
        response=super().form_valid(form)
        profile_instance=Profile(user=self.object)
        profile_instance.save()
        govapp_instance=GovernmentAppointment(user=self.object)
        govapp_instance.save()

        return response 