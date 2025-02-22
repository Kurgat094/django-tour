from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name='home'),
    path('categories', categories, name='categories'),
    path('contests', contests, name='contests'),
    path('contestdetails', contestdetails, name='contestdetails'),
    path('users', users, name='users'),
    path('signin', signin, name='signin'),
    path('signup', signup, name='signup'),
]
