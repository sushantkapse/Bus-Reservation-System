from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Bus(models.Model):
    bus_id = models.AutoField(primary_key=True)
    bus_no = models.CharField(max_length=20)
    capacity = models.IntegerField()
    start_point = models.CharField(max_length=100)
    destination = models.CharField(max_length=100)
    seat_price = models.DecimalField(max_digits=8, decimal_places=2)
    available_seats = models.IntegerField(default=40)



class Booking(models.Model):
  
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    bus = models.ForeignKey(Bus, on_delete=models.CASCADE)
    booking_date = models.DateTimeField(auto_now_add=True)
    seats = models.IntegerField()
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)