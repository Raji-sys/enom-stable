from django.urls import path,include
from .views import CustomLoginView, ProfileDetailView, DocumentationView, UserRegistrationView
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('',include('django.contrib.auth.urls')),
    path('documentation/<int:pk>/', DocumentationView.as_view(), name='doc'),
    path('profile/<str:username>/', ProfileDetailView.as_view(), name='profile_details'),
]
