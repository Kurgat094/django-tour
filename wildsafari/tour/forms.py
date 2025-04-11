from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from .models import *
from datetime import datetime

class SignUpForm(UserCreationForm):
    email = forms.EmailField(
        max_length=255,
        required=True,
        help_text="Required. Enter a valid email address."
    )

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

# placeholder for registration form
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].widget.attrs.update({"placeholder": "Username"})
        self.fields["email"].widget.attrs.update({"placeholder": "Email"})
        self.fields["password1"].widget.attrs.update({"placeholder": "Password"})
        self.fields["password2"].widget.attrs.update({"placeholder": "Confirm Password"})

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already in use. Please use a different one.")
        return email


class OtpForm(forms.ModelForm):
   class Meta:
      model=Otp
      fields=['otp','is_verified']




class BookingForm(forms.ModelForm):
    

    date_of_visit = forms.DateField(
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'})
    )

    time_of_visit = forms.TimeField(
        widget=forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'})
    )

    class Meta:
        model = Booking
        fields = ['name', 'contactname', 'email', 'phone', 'place_of_visit','tour_package', 'date_of_visit', 'end_of_visit', 'time_of_visit' ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.fields["name"].widget.attrs.update({"placeholder": "Name"})
        self.fields["contactname"].widget.attrs.update({"placeholder": "Contact Name"})
        self.fields["email"].widget.attrs.update({"placeholder": "Email"})
        self.fields["phone"].widget.attrs.update({"placeholder": "Phone"})
        self.fields["date_of_visit"].widget.attrs.update({"placeholder": "Date of Visit"})
        self.fields["end_of_visit"].widget.attrs.update({"placeholder": "End of Visit"})
        self.fields["time_of_visit"].widget.attrs.update({"placeholder": "Time of Visit"})
        self.fields["place_of_visit"].widget.attrs.update({"placeholder": "Place of Visit"})
        self.fields["tour_package"].widget.attrs.update({"placeholder": "Tour Package"})   


    def clean_group_size(self):
        group_size = self.cleaned_data.get('group_size')
        if group_size < 2:
            raise forms.ValidationError("Group size must be at least 2.")
        return group_size
    

class SoloBookingForm(forms.ModelForm):

    TOUR_PACKAGE_CHOICES = [
        ('basic', 'Basic Package'),
        ('premium', 'Premium Package'),
        ('luxury', 'Luxury Package'),
    ]

    PAYMENT_METHOD_CHOICES = [
        ('mpesa', 'M-Pesa'),
        ('credit_card', 'Credit Card'),
        ('debit_card', 'Debit Card'),
        ('paypal', 'Paypal'),
    ]
    s_tour_package = forms.ChoiceField(
        choices=[('', 'Select a Tour Package')] + TOUR_PACKAGE_CHOICES, 
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    s_payment_method = forms.ChoiceField(
        choices=[('', 'Select Payment Method')] + PAYMENT_METHOD_CHOICES, 
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    s_date_of_visit = forms.DateField(
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'})
    )

    s_time_of_visit = forms.TimeField(
        widget=forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'})
    )

    class Meta:
        model = SoloBooking
        fields = ['contact_name', 's_email', 's_phone', 's_date_of_visit', 's_time_of_visit', 's_place_of_visit', 's_tour_package', 's_payment_method' ,'s_status']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["contact_name"].widget.attrs.update({"placeholder": "Contact Name"})
        self.fields["s_email"].widget.attrs.update({"placeholder": "Email"})
        self.fields["s_phone"].widget.attrs.update({"placeholder": "Phone"})
        self.fields["s_date_of_visit"].widget.attrs.update({"placeholder": "Date of Visit"})
        self.fields["s_time_of_visit"].widget.attrs.update({"placeholder": "Time of Visit"})
        self.fields["s_place_of_visit"].widget.attrs.update({"placeholder": "Place of Visit"})
        self.fields["s_tour_package"].widget.attrs.update({"placeholder": "Tour Package"}) 
    
    


    

class TourismSiteForm(forms.ModelForm):
    class Meta:
        model = TourismSite
        fields = ['name', 'description','place','image']