from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Otp(models.Model): 
    user=models.CharField(max_length=10,blank=True,null=True)
    otp=models.CharField(max_length=6)
    is_verified=models.IntegerField(default=0)
    created_at=models.DateTimeField(auto_now_add=True)



class Booking(models.Model):
    name=models.CharField(max_length=100)
    contactname = models.CharField(max_length=255,)  # Choose an appropriate default
    email=models.EmailField()
    phone=models.CharField(max_length=10)
    date_of_visit=models.DateField()
    time_of_visit=models.TimeField()
    place_of_visit=models.CharField(max_length=100)
    tour_package=models.CharField(max_length=100)

    status = models.TextField(default='Pending',max_length=100)
    
class SoloBooking(models.Model):
    id = models.AutoField(primary_key=True)
    contact_name = models.CharField(max_length=255,)  # Choose an appropriate default
    s_email=models.EmailField()
    s_phone=models.CharField(max_length=10)
    s_date_of_visit=models.DateField()
    s_time_of_visit=models.TimeField()
    s_place_of_visit=models.CharField(max_length=100)
    s_tour_package=models.CharField(max_length=100)
    s_payment_method=models.CharField(max_length=100)
    s_status = models.TextField(default='Pending',max_length=100)
    


class TourismSite(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(default="No description available") 
    place=models.CharField(max_length=200)
    image = models.ImageField()
    details = models.TextField(default="No details available")

    def __str__(self):
        return self.name

class Itinerary(models.Model):
    name = models.ForeignKey(TourismSite, on_delete=models.CASCADE, related_name="itinerary")
    day_number = models.PositiveIntegerField()
    title = models.CharField(max_length=255)
    description = models.TextField()
    meals = models.CharField(max_length=50, help_text="E.g., B, L & D for Breakfast, Lunch & Dinner")

    class Meta:
        ordering = ['day_number']

    def __str__(self):
        return f"Day {self.day_number}: {self.title}"
    

class TanzaniaSite(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(default="No description available") 
    place=models.CharField(max_length=200)
    image = models.ImageField()

    def __str__(self):
        return self.name
