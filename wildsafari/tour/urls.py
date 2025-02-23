from django.urls import path
from .views import *
from django.contrib import admin

urlpatterns = [
    path('', home, name='home'),
    path('categories', categories, name='categories'),
    path('contests', contests, name='contests'),
    path('contestdetails', contestdetails, name='contestdetails'),
    path('users', users, name='users'),
    path('signin', signin, name='signin'),
    path('signup', signup, name='signup'),
    path('signout', signout, name='signout'),
    path('otp', otp, name='otp'),
    
    path('password_sent',auth_views.PasswordResetDoneView.as_view(template_name='confirmresetlink.html'),name='password_reset_done'),
    path('passwordreset',auth_views.PasswordResetView.as_view(template_name='forgotpassword.html'),name='password_reset'),
    path('password_reset_confirm/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name='resetpassword.html'),name='password_reset_confirm'),
    path('password_reset_complete',auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'),name='password_reset_complete'),


    # Admin urls
    path('approvals', approvals, name='approvals'),
    path('adminhome', adminhome, name='adminhome'),

]
