from django.urls import path
from . import views
app_name='bloodbankapp'
urlpatterns=[
    path('',views.home,name='home'),
    path('signup/',views.signup,name='signup'),
    path('login/',views.login,name='login'),
    # path('profile/',views.profile,name='profile'),
    path('patientdetails/',views.patientdetails,name='patientdetails'),
    path('donordetails/',views.donordetails,name='donordetails'),
    path('success',views.success,name='success'),
    path('adminview/',views.adminview,name='adminview'),
    path('p_signup/',views.p_signup,name='p_signup'),
    path('plogin/',views.p_login,name='p_login'),
    path('patient_dashboard/',views.patient_dashboard,name='patient_dashboard'),
    path('approve/<int:patient_id>/', views.approve_patient, name='approve_patient'),



]