from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
# Create your models here.


class Otp(models.Model): 
    user=models.CharField(max_length=10,blank=True,null=True)
    otp=models.CharField(max_length=6)
    is_verified=models.IntegerField(default=0)
    created_at=models.DateTimeField(auto_now_add=True)


def get_end_of_visit():
    return timezone.now() + timedelta(days=7)
class Booking(models.Model):
    name=models.CharField(max_length=100)
    contactname = models.CharField(max_length=255,)  # Choose an appropriate default
    email=models.EmailField()
    phone=models.CharField(max_length=10)
    date_of_visit=models.DateField()
    end_of_visit = models.DateTimeField()   
    time_of_visit=models.TimeField()
    place_of_visit=models.CharField(max_length=100)
    tour_package=models.CharField(max_length=100,default="Basic Package")
    status = models.TextField(default='Pending',max_length=100)
    
class SoloBooking(models.Model):
    id = models.AutoField(primary_key=True)
    contact_name = models.CharField(max_length=255,)  # Choose an appropriate default
    s_email=models.EmailField()
    s_phone=models.CharField(max_length=10)
    s_date_of_visit=models.DateField()
    s_time_of_visit=models.TimeField()
    s_place_of_visit=models.CharField(max_length=100)

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
    meals = models.TextField( blank=True, help_text="E.g., B, L & D for Breakfast, Lunch & Dinner")

    class Meta:
        ordering = ['name']

    def __str__(self):
        return f" Day {self.day_number} -{self.name.name} "
    

class TanzaniaSite(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(default="No description available") 
    place=models.CharField(max_length=200)
    image = models.ImageField()
    details=models.TextField(default="No details available")

    def __str__(self):
        return self.name

class Tanzania_Itinerary(models.Model):
    name=models.ForeignKey(TanzaniaSite,on_delete=models.CASCADE,related_name="Tz_itinerary") 
    day_number=models.PositiveIntegerField()
    title=models.CharField(max_length=255)  
    description=models.TextField()
    meals=models.TextField(help_text="E.g., B, L & D for Breakfast, Lunch & Dinner")

    class Meta:
        ordering = ['name']

    def __str__(self):
        return f" Day {self.day_number} -{self.name.name} "

# Uganda
class UgandaSite(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(default="No description available") 
    place=models.CharField(max_length=200)
    image = models.ImageField()
    details=models.TextField(default="No details available")

    def __str__(self):
        return self.name
class Uganda_Itinerary(models.Model):
    name=models.ForeignKey(UgandaSite,on_delete=models.CASCADE,related_name="Ug_itinerary") 
    day_number=models.PositiveIntegerField()
    title=models.CharField(max_length=255)  
    description=models.TextField()
    meals=models.TextField(help_text="E.g., B, L & D for Breakfast, Lunch & Dinner")

    class Meta:
        ordering = ['name']

    def __str__(self):
        return f" Day {self.day_number} -{self.name.name} "
# contact messages

class ContactMessage(models.Model):
    name = models.CharField(max_length=255)
    telephone = models.CharField(max_length=20)
    email = models.EmailField()
    subject = models.CharField(max_length=255, blank=True, null=True)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.subject if self.subject else 'No Subject'}"