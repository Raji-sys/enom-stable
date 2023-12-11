from django.urls import path,include
from .views import CustomLoginView, ProfileDetailView, DocumentationView, UserRegistrationView, CustomLogoutView, UpdateUserView,UpdateProfileView, UpdateGovappView
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('documentation/<int:pk>/', DocumentationView.as_view(), name='doc'),
    path('profile/<str:username>/', ProfileDetailView.as_view(), name='profile_details'),
    path('update-user/<int:pk>/', UpdateUserView.as_view(), name='update_user'),
    path('update-profile/<int:pk>/', UpdateProfileView.as_view(), name='update_profile'),
    path('update-govapp/<int:pk>/', UpdateGovappView.as_view(), name='update_govapp'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('',include('django.contrib.auth.urls')),
]
