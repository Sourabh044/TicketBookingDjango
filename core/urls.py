from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    path('', HomePage, name='Home'),
    path('login/', UserLogin, name='Home'),
    path('signup/', signup, name='signup'),
    path('verify/', UserVerifyView, name='User Verify'),
    path('profile/', UserProfileView, name='UserProfile'),
    path('password/', UserPasswordChange, name='UserPasswordChange'),
    path('password-reset/', UserPasswordReset, name='UserPasswordReset'),

]
