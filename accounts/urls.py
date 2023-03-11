from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('', views.dashboard, name='dashboard'),
    path('forgot_pass/', views.forgot_pass, name='forgot_pass'),
    path('reset_pass_validate/<uidb64>/<token>', views.reset_pass_validate, name='reset_pass_validate'),
    path('reset_pass_confirm/', views.reset_pass_confirm, name='reset_pass_confirm'),
    path('activate/<uidb64>/<token>', views.activate, name='activate'),

]
