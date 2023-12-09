from django.urls import path,include
from .views import CustomLoginView, ProfileDetailView, DocumentationView, UserRegistrationView, CustomLogoutView
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('documentation/<int:pk>/', DocumentationView.as_view(), name='doc'),
    path('profile/<str:username>/', ProfileDetailView.as_view(), name='profile_details'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('',include('django.contrib.auth.urls')),
]
