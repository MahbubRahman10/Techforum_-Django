from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include
from . import views

from django.contrib.auth import views as auth_views 

urlpatterns = [
    path('register', views.register, name='Register-Page'),
    path('login', views.login, name='Login-Page'),
    path('logout', views.logout, name='Logout-Page'),


    url(r'^oauth/', include('social_django.urls', namespace='social')),

    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='reset.html'), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='resetdone.html'), name='password_reset_done'),
    path('password_reset/confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='acc_password_reset.html'), name='password_reset_confirm'),
    path('password_reset/complete/', auth_views.PasswordResetCompleteView.as_view(template_name='resetcomplete.html'), name='password_reset_complete'),
    

    path('user/profile/<int:pk>/', views.userprofile, name='Userprofile-Page'),
    path('user/question/<int:pk>/', views.userquestion, name='Userquestion-Page'),
    path('user/profile/setting/<int:pk>/', views.profilesetting, name='Profilesetting-Page'),
    path('user/profile/setting/password/<int:pk>/', views.passwordsetting, name='Passwordsetting-Page'),

    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.activate, name='activate'),
]
