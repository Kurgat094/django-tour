from django.shortcuts import render, redirect, get_object_or_404
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
            return render(request, 'contests.html', )

    return render(request, 'contests.html', {"form": form})

@csrf_exempt
def contestdetails(request):
    form = SoloBookingForm()  # Correctly instantiate the form
    if request.method == "POST":
        form = SoloBookingForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Booking successful")
        else:
            messages.error(request, "Booking failed")
            return render(request, 'contest-details.html',)

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
                    elif role.name=='user':
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
    bookings = Booking.objects.all()
    solo_bookings = SoloBooking.objects.all()
    
    context = {
        'bookings': bookings,
        'solo_bookings': solo_bookings
    }
    return render(request, 'admin/approvals.html', context)


def group_approval(request, id):
    booking = get_object_or_404(Booking, id=id)  # Fetch the booking safely
    booking.status = "Approved"
    booking.save()

    subject = "Booking Approved"
    message = f"""Hello Adventurer!  

Great news! 🎉 Your booking with Stevensons Trails Company has been **approved**!  

🗺️ Get ready to embark on an unforgettable adventure filled with breathtaking views and thrilling experiences.  

📅 Your approved booking details are confirmed, and we can't wait to host you! If you have any questions or need further assistance, feel free to reach out. 

Your Tour will be on {booking.date_of_visit} at {booking.time_of_visit} at {booking.place_of_visit}

Thanks for choosing us—your adventure starts now!

If you didn’t make this booking, please contact us immediately.  

Thanks for choosing us—your adventure starts now!  

Happy Trails,  
🌲 The Stevensons Trails Team 🌲  
"""

    from_email = "tobiaskipkogei@gmail.com"
    recipient_list = [booking.email]  # Use the actual email from booking

    send_mail(subject, message, from_email, recipient_list)

    return redirect('approvals')

def solo_approval(request,id):
    solo_booking = get_object_or_404(SoloBooking, id=id)  # Fetch the booking safely
    solo_booking.status = "Approved"
    solo_booking.save()

    subject = "Booking Approved"
    message = f"""Hello Adventurer!  

Great news! 🎉 Your booking with Stevensons Trails Company has been **approved**!  

🗺️ Get ready to embark on an unforgettable adventure filled with breathtaking views and thrilling experiences.  

📅 Your approved booking details are confirmed, and we can't wait to host you! If you have any questions or need further assistance, feel free to reach out.  

Your Tour will be on {solo_booking.s_date_of_visit} at {solo_booking.s_time_of_visit} at {solo_booking.s_place_of_visit} 

Thanks for choosing us—your adventure starts now!

If you didn’t make this booking, please contact us immediately.  

Thanks for choosing us—your adventure starts now!  

Happy Trails,  
🌲 The Stevensons Trails Team 🌲  
"""

    from_email = "tobiaskipkogei@gmail.com"
    recipient_list = [solo_booking.s_email]  # Use the actual email from booking

    send_mail(subject, message, from_email, recipient_list)
    
    return redirect('approvals')


def group_denial(request,id):
    booking = get_object_or_404(Booking, id=id)  # Fetch the booking safely
    booking.status = "Decline"
    booking.save()

    subject = "Booking Denied"
    message = f"""Hello Adventurer,  

We regret to inform you that your booking for { booking.place_of_visit }with **Stevensons Trails Company** has not been approved. 😞  

Unfortunately, due to [reason, e.g., unavailability, scheduling conflicts, or other circumstances], we are unable to confirm your booking at this time.  

We sincerely apologize for any inconvenience this may cause. If you’d like to reschedule or explore other available options, please feel free to reach out to us.  

If you have any questions or need assistance, we're here to help!  

We hope to welcome you on an adventure with us soon.  

Best Regards,  
🌲 The Stevensons Trails Team 🌲  
"""

    from_email = "tobiaskipkogei@gmail.com"
    recipient_list = [booking.email]  # Use the actual email from booking

    send_mail(subject, message, from_email, recipient_list)

    return redirect('approvals')
    
def solo_denial(request,id):
    solo_booking = get_object_or_404(SoloBooking, id=id)  # Fetch the booking safely
    solo_booking.s_status = "Decline"
    solo_booking.save()

    subject = "Booking Denied"
    message = f"""Hello Adventurer,  

We regret to inform you that your booking  for { solo_booking.s_place_of_visit } tour with **Stevensons Trails Company** has not been approved. 😞  

Unfortunately, due to [reason, e.g., unavailability, scheduling conflicts, or other circumstances], we are unable to confirm your booking at this time.  

We sincerely apologize for any inconvenience this may cause. If you’d like to reschedule or explore other available options, please feel free to reach out to us.  

If you have any questions or need assistance, we're here to help!  

We hope to welcome you on an adventure with us soon.  

Best Regards,  
🌲 The Stevensons Trails Team 🌲  
"""
    
    from_email = "tobiaskipkogei@gmail.com"
    recipient_list = [solo_booking.s_email]  

    send_mail(subject, message, from_email, recipient_list)

    return redirect('approvals')