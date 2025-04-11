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
from django.core.mail import send_mail, EmailMultiAlternatives
import random
import logging
from django.views.decorators.csrf import csrf_exempt
from django.utils.html import strip_tags
from django.db.models import Q
from django.core.signing import Signer
from django.conf import settings
from django.shortcuts import redirect
import stripe

stripe.api_key = settings.STRIPE_SECRET_KEY
signer = Signer()
# Ensure 'booking' is defined before using it
# Example: Replace 'booking.id' with a valid booking instance or remove this code if not needed
# signed_id = signer.sign(booking.id)
# payment_url = f"https://yourwebsite.com/payment/{signed_id}/"



logger = logging.getLogger(__name__)


from django.shortcuts import get_object_or_404
@csrf_exempt
def create_checkout_session(request, booking_id):
    # Fetch the booking instance using the booking_id
    booking = get_object_or_404(Booking, id=booking_id)

    # Extract the amount from the booking instance
    # Assuming the amount is stored in cents (e.g., 1000 for $10.00)
    amount = int(booking.amount*100) # Convert to cents

    # Create a Stripe Checkout session
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price_data': {
                'currency': 'usd',
                'product_data': {
                    'name': f'Tour Package: {booking.tour_package}',  # Use the tour package name
                },
                'unit_amount': amount,  # Pass the amount dynamically
            },
            'quantity': 1,
        }],
        mode='payment',
        success_url=request.build_absolute_uri('/success/'),  # Replace with your success URL
        cancel_url=request.build_absolute_uri('/cancel/'),    # Replace with your cancel URL
    )

    # Redirect the user to the Stripe Checkout page
    return redirect(session.url, code=303)

# Create your views here.
@csrf_exempt
def home(request):
    tourism_sites = TourismSite.objects.filter(itinerary__isnull=False).distinct()
    tourism_sites1 = TourismSite.objects.filter(itinerary__isnull=True)[:4]
    tourism_sites_2 = TourismSite.objects.all()[4:30]  # Fetch the next 10 tourism sites
    itinaries = Itinerary.objects.all()
    return render(request, 'index.html', {'tourism_sites': tourism_sites  , 'itinaries': itinaries , 'tourism_sites_2': tourism_sites_2 , 'tourism_sites1': tourism_sites1})

@csrf_exempt
def about(request):
    return render(request, 'about_us.html')

@csrf_exempt
def categories(request):
    # to show the first 8 tourism sites

    tourism_sites = TourismSite.objects.all()

    tourism_sites1 = TanzaniaSite.objects.all()
    tourism_sites2 = UgandaSite.objects.all()
    return render(request, 'categories.html', {'tourism_sites': tourism_sites, 'tourism_sites1': tourism_sites1, 'tourism_sites2': tourism_sites2})

@csrf_exempt
def book(request, site_id):
    # Get the tourism site or return a 404 error if not found
    tourism_site = get_object_or_404(TourismSite, id=site_id)
    day_count = tourism_site.itinerary.count()
    # Get the itineraries for the selected tourism site
    itineraries = Itinerary.objects.filter(name=tourism_site)

    form = BookingForm()  # Correctly instantiate the form
    if request.method == "POST":
        form = BookingForm(request.POST)
        if form.is_valid():
            Booking.objects.create(
                name=form.cleaned_data['name'],
                contactname=form.cleaned_data['contactname'],
                email=form.cleaned_data['email'],
                phone=form.cleaned_data['phone'],
                place_of_visit=tourism_site.place,  # Automatically set from tourism_site
                tour_package=form.cleaned_data['tour_package'],
                date_of_visit=form.cleaned_data['date_of_visit'],
                end_of_visit=form.cleaned_data['end_of_visit'],
                time_of_visit=form.cleaned_data['time_of_visit']
            )
            messages.success(request, "Booking successful!")
            return redirect('home')
        else:
            messages.error(request, "Booking failed")
            return render(request, 'contests.html' ,{
                'tourism_site': tourism_site,
                'itineraries': itineraries,
                'day_count': day_count,
                'form_data': request.POST,
            })
    
    return render(request, 'contests.html', {
        'tourism_site': tourism_site,
        'itineraries': itineraries,
        'day_count': day_count,
        'form': form,
    })

def tzbook(request, site_id):
    # Get the tourism site or return a 404 error if not found
    tourism_site = get_object_or_404(TanzaniaSite, id=site_id)
    day_count = tourism_site.Tz_itinerary.count()
    # Get the itineraries for the selected tourism site
    itineraries = Tanzania_Itinerary.objects.filter(name=tourism_site)

    form = BookingForm()  # Correctly instantiate the form
    if request.method == "POST":
        form = BookingForm(request.POST)
        if form.is_valid():
            Booking.objects.create(
                name=form.cleaned_data['name'],
                contactname=form.cleaned_data['contactname'],
                email=form.cleaned_data['email'],
                phone=form.cleaned_data['phone'],
                place_of_visit=tourism_site.place,  # Automatically set from tourism_site
                tour_package=form.cleaned_data['tour_package'],
                date_of_visit=form.cleaned_data['date_of_visit'],
                end_of_visit=form.cleaned_data['end_of_visit'],
                time_of_visit=form.cleaned_data['time_of_visit']
            )
            messages.success(request, "Booking successful!")
            return redirect('home',)
        else:
            messages.error(request, "Booking failed")
            return render(request, 'contests.html', )
    
    return render(request, 'contests.html', {
        'tourism_site': tourism_site,
        'itineraries': itineraries,
        'day_count': day_count,
        'form': form,
    })

@csrf_exempt
def ugbook(request, site_id):
    # Get the tourism site or return a 404 error if not found
    tourism_site = get_object_or_404(UgandaSite, id=site_id)
    day_count = tourism_site.Ug_itinerary.count()
    # Get the itineraries for the selected tourism site
    itineraries = Uganda_Itinerary.objects.filter(name=tourism_site)

    form = BookingForm()  # Correctly instantiate the form
    if request.method == "POST":
        form = BookingForm(request.POST)
        if form.is_valid():
            Booking.objects.create(
                name=form.cleaned_data['name'],
                contactname=form.cleaned_data['contactname'],
                email=form.cleaned_data['email'],
                phone=form.cleaned_data['phone'],
                place_of_visit=tourism_site.place,  # Automatically set from tourism_site
                tour_package=form.cleaned_data['tour_package'],
                date_of_visit=form.cleaned_data['date_of_visit'],
                end_of_visit=form.cleaned_data['end_of_visit'],
                time_of_visit=form.cleaned_data['time_of_visit']
            )
            messages.success(request, "Booking successful!")
            return redirect('home',)
        else:
            messages.error(request, "Booking failed")
            return render(request, 'contests.html', )
        
    return render(request, 'contests.html', {
        'tourism_site': tourism_site,
        'itineraries': itineraries,
        'day_count': day_count,
        'form': form,
    })

@csrf_exempt
def contact_messages(request):
    if request.method == "POST":
        name = request.POST.get("name")
        telephone = request.POST.get("telephone")
        email = request.POST.get("email")
        subject = request.POST.get("subject", "")
        message = request.POST.get("message")

        # Save the message to the database
        ContactMessage.objects.create(
            name=name,
            telephone=telephone,
            email=email,
            subject=subject,
            message=message
        )

        messages.success(request, "Your message has been sent successfully!")
        return redirect(request.META.get("HTTP_REFERER", "contests"))


    return render(request, "contests.html")


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

@csrf_exempt
def users(request):
    return render(request, 'contact.html')

@csrf_exempt
def terms_conditions(request):
    return render(request, 'terms_conditions.html')


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
                        return redirect('approvals')
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


@csrf_exempt
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
@csrf_exempt
def add_tourism_site(request):
    if request.method == 'POST':
        form = TourismSiteForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home')  # Redirect to a list view or success page
    else:
        form = TourismSiteForm()
    return render(request, 'admin/tourismattractionsites.html', {'form': form})



@csrf_exempt
def adminhome(request):
    return render(request, 'admin/adminhome.html')

@csrf_exempt
def approvals(request):
    bookings = Booking.objects.all()
    solo_bookings = SoloBooking.objects.all()
    search_query = request.GET.get('search', '')  # Get the search query from the URL
    if search_query:
        # Filter bookings by matching the search query in any of the relevant fields
        bookings = Booking.objects.filter(
            Q(name__icontains=search_query) |
            Q(contactname__icontains=search_query) |
            Q(email__icontains=search_query) |
            Q(phone__icontains=search_query) |
            Q(place_of_visit__icontains=search_query) |
            Q(date_of_visit__icontains=search_query) |
            Q(end_of_visit__icontains=search_query) |
            Q(time_of_visit__icontains=search_query) |
            Q(tour_package__icontains=search_query) |
            Q(status__icontains=search_query)
        )
    else:
        # If no search query, return all bookings
        bookings = Booking.objects.all()
    
    context = {
        'bookings': bookings,
        'solo_bookings': solo_bookings
    }
    return render(request, 'admin/approvals.html', context)

from django.urls import reverse

@csrf_exempt
def bookapproval(request, id):
    booking = get_object_or_404(Booking, id=id)  # Fetch the booking safely
    if request.method == "POST":
        # Get the amount entered by the admin
        amount = request.POST.get("amount")
        if amount:
            try:
                # Save the entered amount to the booking
                booking.amount = float(amount)  # Convert to float and save
                booking.status = "Approved"
                booking.save()
            except ValueError:
                messages.error(request, "Invalid amount entered.")
                return redirect('approvals')
        else:
            messages.error(request, "Amount is required.")
            return redirect('approvals')
    

    payment_urls = f"https://stevensons-trails-company-1n65.onrender.com/buy/{booking.id}"
    payment=request.build_absolute_uri(reverse('buy', args=[booking.id]))


    subject = 'Your Inquiry Has Been Approved - Stevensons Trails'
    html_content = f"""
    <html>
    <head>
        <style>
            body {{
                font-family: 'Segoe UI', sans-serif;
                background-color: #f5f7fa;
                padding: 20px;
                color: #333;
            }}
            .container {{
                max-width: 600px;
                margin: auto;
                background: #fff;
                border-radius: 8px;
                padding: 30px;
                background-color: #ecf0f1;
                box-shadow: 0 0 10px rgba(0,0,0,0.1);
            }}
            .header {{
                background-color: #2c3e50;
                padding: 20px;
                color: white;
                border-radius: 8px 8px 0 0;
                text-align: center;
            }}
            .section {{
                margin-top: 20px;
            }}
            .section h3 {{
                color: #2c3e50;
            }}
            .card {{
                background-color: #D86F2C;
                padding: 15px;
                border-radius: 8px;
                margin: 10px 0;
                color: white;
                box-shadow: 0 2px 5px rgba(0,0,0,0.05);
            }}
            .btn {{
                display: inline-block;
                padding: 10px 20px;
                background-color: #2980b9;
                color: white;
                text-decoration: none;
                border-radius: 5px;
                margin-top: 20px;
                text-align: center;
                
            }}
            .footer {{
                margin-top: 30px;
                color: #777;
                text-align: center;
                font-size: 16px;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h2>🎉 Inquiry Approved!</h2>
                <p>Stevensons Trails Company</p>
            </div>

            <div class="section">
                <p>Hello Adventurer,</p>
                <p>We're thrilled to let you know your Inquiry has been <strong>approved</strong>!</p>

                <div class="section">
                    <h3>📅 Your Tour Details</h3>
                    <p><strong>Date of Tour:</strong> {booking.date_of_visit}</p>
                    <p><strong>End of Tour:</strong> {booking.end_of_visit}</p>
                    <p><strong>Time:</strong> {booking.time_of_visit}</p>
                    <p><strong>Location:</strong> {booking.place_of_visit}</p>
                    <p><strong>Package:</strong> {booking.tour_package} Package</p>
                    <p><strong>Amount to Pay USD:</strong> ${booking.amount}</p>
                    <p><strong>Amount to Pay Ksh:</strong> Ksh {booking.amount *  134.8744:.2f}</p>
                </div>

                <div class="section">
                    <h3>💳 Payment Methods</h3>
                    <div class="card">
                        <strong>Mastercard</strong><br/>
                        Acc No: 123456789
                    </div>
                    <div class="card">
                        <strong>Visa</strong><br/>
                        Acc No: 987654321
                    </div>
                </div>

               <a href="{payment}" class="btn">Make Payment</a>
               <a href="{payment_urls}" class="btn">Make Payment</a>
               

            </div>

            <div class="footer">
                <p>If you didn’t make this Inquiry, please contact us immediately.</p>
                <p>🌲 Thanks for choosing Stevensons Trails – Your adventure starts now! 🌲</p>
            </div>
        </div>
    </body>
    </html>
    """
    text_content = strip_tags(html_content)

    msg = EmailMultiAlternatives(subject, text_content, 'tobiaskipkogei@gmail.com', [booking.email])
    msg.attach_alternative(html_content, "text/html")
    msg.send()
    return redirect('approvals')

@csrf_exempt
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

@csrf_exempt
def bookdenial(request,id):
    booking = get_object_or_404(Booking, id=id)  # Fetch the booking safely
    booking.status = "Decline"
    booking.save()

    
    subject = "Inquiry Declined - Stevensons Trails"
    html_content = f"""
<html>
<head>
    <style>
        body {{
            font-family: 'Segoe UI', sans-serif;
            background-color: #f5f7fa;
            padding: 20px;
            color: #333;
        }}
        .container {{
            max-width: 600px;
            margin: auto;
            background: #fff;
            border-radius: 8px;
            padding: 30px;
            box-shadow: 0 0 10px rgba(0,0,0,0.1);
            background-color: #ecf0f1;
        }}
        .header {{
            background-color: #e74c3c;
            padding: 20px;
            color: white;
            border-radius: 8px 8px 0 0;
            text-align: center;
        }}
        .section {{
            margin-top: 20px;
        }}
        .section h3 {{
            color: #e74c3c;
        }}
        .card {{
            background-color: #ecf0f1;
            padding: 15px;
            border-radius: 8px;
            margin: 10px 0;
            box-shadow: 0 2px 5px rgba(0,0,0,0.05);
        }}
        .footer {{
            margin-top: 30px;
            color: #777;
            text-align: center;
            font-size: 16px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h2>⚠️ Inquiry Denied</h2>
            <p>Stevensons Trails Company</p>
        </div>

        <div class="section">
            <p>Hello Adventurer,</p>
            <p>We regret to inform you that your Inquiry for <strong>{booking.place_of_visit}</strong> with <strong>Stevensons Trails Company</strong> has not been approved. 😞</p>
            <p>Unfortunately, due to <strong>[reason]</strong>, we are unable to confirm your inquiry at this time.</p>

            <div class="section">
                <h3>💡 Next Steps</h3>
                <p>If you'd like to reschedule or explore other available options, please feel free to reach out to us.</p>
            </div>

            <div class="footer">
                <p>If you have any questions or need assistance, we're here to help!</p>
                <p>🌲 Thanks for considering Stevensons Trails – we hope to welcome you on an adventure soon! 🌲</p>
            </div>
        </div>
    </body>
</html>
"""
    text_content = strip_tags(html_content)

    from_email = "tobiaskipkogei@gmail.com"
    recipient_list = [booking.email]  # Use the actual email from booking

    msg = EmailMultiAlternatives(subject, text_content, from_email, recipient_list)
    msg.attach_alternative(html_content, "text/html")
    msg.send()

    return redirect('approvals')

@csrf_exempt    
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


@csrf_exempt
def payment(request,id):
    booking = get_object_or_404(Booking, pk=id)
    return render(request, 'payment/payment.html' ,{
        'booking': booking,
    })



# Other Site Views And Services
@csrf_exempt
def tanzania(request):
    tourism_sites = TanzaniaSite.objects.filter(Tz_itinerary__isnull=False).distinct()
    tourism_sites1 = TanzaniaSite.objects.filter(Tz_itinerary__isnull=True)[:8]
    tourism_sites_2 = TanzaniaSite.objects.all()[8:30]  # Fetch the next 10 tourism sites
    itinaries = Tanzania_Itinerary.objects.all()
    return render(request, 'tanzania.html',{ 'tourism_sites': tourism_sites , 'itinaries': itinaries , 'tourism_sites_2': tourism_sites_2 , 'tourism_sites1': tourism_sites1})  

@csrf_exempt
def kenya(request):
    return render(request, 'categories.html')

@csrf_exempt
def uganda(request):
    tourism_sites = UgandaSite.objects.filter(Ug_itinerary__isnull=False).distinct()
    tourism_sites1 = UgandaSite.objects.filter(Ug_itinerary__isnull=True)[:8]
    tourism_sites_2 = UgandaSite.objects.all()[8:30]  # Fetch the next 10 tourism sites
    itinaries = Uganda_Itinerary.objects.all()
    return render(request, 'uganda.html', { 'tourism_sites': tourism_sites , 'itinaries': itinaries , 'tourism_sites_2': tourism_sites_2 , 'tourism_sites1': tourism_sites1})

@csrf_exempt
def rwanda(request):
    return render(request, 'rwanda.html')


@csrf_exempt
def indianocean(request):
    return render(request, 'indianocean.html')

@csrf_exempt
def mtKenya(request):
    return render(request,'mtKenya.html')
