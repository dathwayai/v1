from django.contrib import admin
from django.urls import path, include
from . import views 
urlpatterns = [
    path('', views.home, name='home'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('chat', views.chat, name='chat'),
    path('analytics', views.analytics, name='analytics'),
    path('course', views.course, name='course'),
    path('notifications', views.notifications, name='notifications'),
    path('profile', views.profile, name='profile'),
    path('settings', views.settings, name='settings'),
    path('login', views.login, name='login'),
    path('sign_out', views.logout, name='logout'),
    path('signup', views.signup, name='signup'),

]