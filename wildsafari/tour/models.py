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
    group_type=models.CharField(max_length=100)
    group_size=models.IntegerField()
    contactname = models.CharField(max_length=255,)  # Choose an appropriate default
    email=models.EmailField()
    phone=models.CharField(max_length=10)
    date_of_visit=models.DateField()
    time_of_visit=models.TimeField()
    place_of_visit=models.CharField(max_length=100)
    tour_package=models.CharField(max_length=100)
    payment_method=models.CharField(max_length=100)
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
    price = models.DecimalField(max_digits=10, decimal_places=2)
    categories = models.CharField(max_length=200)
    image = models.ImageField(upload_to='tourism_sites/')

    def __str__(self):
        return self.name

