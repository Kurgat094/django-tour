from django.urls import path
from .views import *
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [

    path('buy/<int:booking_id>/', create_checkout_session, name='buy'),
    # user urls
    path('', home, name='home'),
    path('explore_us', categories, name='categories'),
    path('booking', contests, name='contests'),
    path('book/<int:site_id>/', book, name='book'),
    path('contestdetails', contestdetails, name='contestdetails'),
    path('contact_us', users, name='users'),
    path('terms_conditions', terms_conditions, name='terms_conditions'),
    path('contact_messages', contact_messages, name='contact_messages'),
    path('about', about, name='about'),


    # payment
    path('payment/<int:id>/', payment, name='payment'),


    # Auth urls
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
    path('approval/<int:id>/', bookapproval, name='approval'),
    path('denial/<int:id>/', bookdenial, name='denial'),
    path('messages',contactmessages, name='contactmessages'),
    path('approve/<int:message_id>/', message_approve, name='message_approve'),
    path('delete/<int:message_id>/', message_delete, name='message_delete'),
    




    # other services

    path('uganda',uganda,name='uganda'),
    path('ugbook/<int:site_id>/',ugbook,name='ugbook'),
    path('kenya',kenya,name='kenya'),
    path('tanzania',tanzania,name='tanzania'),
    path('tzbook/<int:site_id>/',tzbook,name='tzbook'),
    path('rwanda',rwanda,name='rwanda'),
    path('indianocean',indianocean,name='indianocean'),
    path('Mt_Kenya',mtKenya,name="mtKenya")

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)