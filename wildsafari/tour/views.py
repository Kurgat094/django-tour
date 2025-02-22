from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.models import User
from .forms import SignUpForm

# Create your views here.

def home(request):
    return render(request, 'index.html')



def categories(request):
    return render(request, 'categories.html')

def contests(request):
    return render(request, 'contests.html')

def contestdetails(request):
    return render(request, 'contest-details.html')

def users(request):
    return render(request, 'users.html')


# Auth functions

def signin(request):
   
    return render(request, 'login.html')

def signup(request):
    
    return render(request, 'register.html' , {'form': SignUpForm()})