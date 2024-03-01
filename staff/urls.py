from django.urls import path, include
from .views import *
from . import views

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('manage/', views.manage, name='manage'),
    path('staff/', StaffListView.as_view(), name='staff'),

    path('dept/', views.dept, name='dept'),
    path('dept_details/<str:name>/', views.dept_details, name='dept_details'),

    path('dirs/', views.dirs, name='dirs'),
    path('dirs_detail/<str:name>/', views.dirs_details, name='dirs_details'),

    path('report/', views.report, name='report'),

    path('gen_report/', GenReportView.as_view(), name='gen_report'),
    path('gen_pdf/', views.Gen_pdf, name='gen_pdf'),
    path('gen_csvFile/', views.Gen_csv, name='gen_csv'),

    path('qual_report/', views.qual_report, name='qual_report'),
    path('pro_qual_report/', views.pro_qual_report, name='pro_qual_report'),
    path('dis_report/', views.dis_report, name='dis_report'),

    path('stats/', StatsView.as_view(), name='stats'),

    path('notice/', NoticeView.as_view(), name='notice'),
    path('promotion_notice/',NoticePromotionView.as_view(), name='notice_promotion'),
    path('leave_notice/',NoticeLeaveView.as_view(), name='notice_leave'),
    path('retirement_notice/',NoticeRetirementView.as_view(), name='notice_retirement'),

    path('login/', CustomLoginView.as_view(), name='login'),
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('reg/', UserRegView.as_view(), name='reg'),
    path('documentation/<int:pk>/', DocumentationView.as_view(), name='doc'),

    path('profile/<str:username>/',
         ProfileDetailView.as_view(), name='profile_details'),
    path('update-user/<int:pk>/', UpdateUserView.as_view(), name='update_user'),
    path('update-profile/<int:pk>/',
         UpdateProfileView.as_view(), name='update_profile'),

    path('update-govapp/<int:pk>/',
         UpdateGovappView.as_view(), name='update_govapp'),

    path('qualification/<str:username>/',
         QualCreateView.as_view(), name='qual'),
    path('qualification/update/<int:pk>/',
         QualUpdateView.as_view(), name='qual_update'),
    path('qualification/delete/<int:pk>/',
         QualDeleteView.as_view(), name='qual_delete'),

    path('pro-qualification/<str:username>/',
         ProQualCreateView.as_view(), name='pro_qual'),
    path('pro-qualification/update/<int:pk>/',
         ProQualUpdateView.as_view(), name='pro_qual_update'),
    path('pro-qualification/delete/<int:pk>/',
         ProQualDeleteView.as_view(), name='pro_qual_delete'),

    path('promotion/<str:username>/',
         PromotionCreateView.as_view(), name='promotion'),
    path('promotion/update/<int:pk>/',
         PromotionUpdateView.as_view(), name='promotion_update'),
    path('promotion/delete/<int:pk>/',
         PromotionDeleteView.as_view(), name='promotion_delete'),

    path('discipline/<str:username>/',
         DisciplineCreateView.as_view(), name='discipline'),
    path('discipline/update/<int:pk>/',
         DisciplineUpdateView.as_view(), name='discipline_update'),
    path('discipline/delete/<int:pk>/',
         DisciplineDeleteView.as_view(), name='discipline_delete'),

    path('leave/<str:username>/', LeaveCreateView.as_view(), name='leave'),
    path('leave/update/<int:pk>/', LeaveUpdateView.as_view(), name='leave_update'),
    path('leave/delete/<int:pk>/', LeaveDeleteView.as_view(), name='leave_delete'),

    path('execapp/<str:username>/', ExecappCreateView.as_view(), name='execapp'),
    path('execapp/update/<int:pk>/',
         ExecappUpdateView.as_view(), name='execapp_update'),
    path('execapp/delete/<int:pk>/',
         ExecappDeleteView.as_view(), name='execapp_delete'),

    path('retire/<str:username>/', RetireCreateView.as_view(), name='retire'),
    path('retire/update/<int:pk>/',
         RetireUpdateView.as_view(), name='retire_update'),
    path('retire/delete/<int:pk>/',
         RetireDeleteView.as_view(), name='retire_delete'),


    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('', include('django.contrib.auth.urls')),
]
