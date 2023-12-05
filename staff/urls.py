from django.urls import path,include
from .views import *
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('',include('django.contrib.auth.urls')),
]
