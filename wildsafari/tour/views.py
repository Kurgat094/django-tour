from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth.models import Group
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import views as auth_views
from django import forms
from .forms import SignUpForm,OtpForm,TourismSiteForm,BookingForm,SoloBookingForm
from .models import Otp
from .models import *
from .forms import BookingForm
from django.core.mail import send_mail
import random
import logging
from django.views.decorators.csrf import csrf_exempt



logger = logging.getLogger(__name__)

# Create your views here.

def home(request):
    return render(request, 'index.html')



def categories(request):
    return render(request, 'categories.html')

@csrf_exempt
def contests(request):
    form = BookingForm()  # Correctly instantiate the form
    if request.method == "POST":
        form = BookingForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Booking successful")
        else:
            messages.error(request, "Booking failed")
            return render(request, 'contests.html', {"form": form})

    return render(request, 'contests.html', {"form": form})

@csrf_exempt
def contestdetails(request):
    form = SoloBooking
    if request.method == "POST":
        form = SoloBookingForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Booking successful")
            return redirect('home')
        else:
            messages.error(request, "Booking failed")
            return render(request, 'contest-details.html', {"form": form})

    return render(request, 'contest-details.html', {"form": form})


def users(request):
    return render(request, 'users.html')


# Auth functions
@csrf_exempt
def signin(request):
    if request.method=="POST":
       form= AuthenticationForm(request,data=request.POST)
       if form.is_valid():
           username=form.cleaned_data.get('username')
           password=form.cleaned_data.get('password')
           user=authenticate(username=username,password=password)
           if user is not None:
                is_verified=Otp.objects.filter(is_verified=1)
                if is_verified:
                    login(request,user)
                    messages.success(request,f"You have loged in successfully")
                    role=Group.objects.get(user=user)
                    print(role.name)
                    if role.name=='admin':
                        return redirect('adminhome')
                
                    return redirect('home')
                else:
                    messages.error(request,"please verify you accont")
                    return redirect('otp')
    else :
        form=AuthenticationForm()
    return render(request, 'login.html')

@csrf_exempt
def signup(request):
    form=SignUpForm
    if request.method=='POST':
        form=SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            name=form.cleaned_data.get('username')
            group=Group.objects.get(name='user')
            user.groups.add(group)
            user.save()
            otp=random.randint(000000,999999)
            Otp.objects.create(user=user,otp=otp)
            subject = "Successfull Registration Notification"
            message = f"""Hello Adventurer!

            Congratulations! 🎉 You’ve successfully registered an account at Stevensons Trails Company—your gateway to unforgettable adventures!

            But wait... 🕵️‍♂️ Before you embark on this thrilling journey, we need to verify that you're truly you!

            🔑 Your Secret Code (OTP): {otp}

            Use this magical code to unlock your account and start exploring! 🌍✨

            If you didn’t request this, well... either you have a secret twin or someone really wants to be you. 😆

            Thanks for choosing us—your next adventure begins now!

            Happy Trails,
        🌲 The Stevensons Trails Team   🌲
                            """
            from_email = "tobiaskipkogei@gmail.com"  
            recipient_list = [user.email]
            try:
                send_mail(subject, message, from_email, recipient_list)
            except Exception as e:
                logger.error(f"Error sending email: {e}")
            return redirect('otp')
    context={
        "form":form
    }
    return render(request, 'register.html', context)



def signout(request):
    logout(request)
    return redirect('signin')

@csrf_exempt 
def otp(request):
    if request.method=="POST":
        user_otp=request.POST['otp']
        otp=Otp.objects.filter(otp=user_otp)
        if otp:
           is_verified=1
           verify,created=Otp.objects.get_or_create(otp=user_otp)
           verify.is_verified=int(is_verified)
           verify.save()
           return redirect('signin')
        else:
            messages.info(request,'Invalid OTP')
            return render(request,'otp')
    return render(request, 'otp.html')



# Admin Roles

def add_tourism_site(request):
    if request.method == 'POST':
        form = TourismSiteForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home')  # Redirect to a list view or success page
    else:
        form = TourismSiteForm()
    return render(request, 'admin/tourismattractionsites.html', {'form': form})




def adminhome(request):
    return render(request, 'admin/adminhome.html')

def approvals(request):
    return render(request, 'admin/approvals.html')