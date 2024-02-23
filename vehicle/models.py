from django.db import models
from django.contrib.auth.models import AbstractUser,Group,Permission,User
from django.db.models.signals import post_save
from django.dispatch import receiver
import uuid
from vehicle.manager import *
from django.contrib.auth import get_user_model



# Create your models her

class User(AbstractUser):
    # Add your custom fields if any
  
    email=models.EmailField(max_length=200,unique=True)
    otp= models.CharField(max_length=4,null=True,blank=True)


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('username',)

    objects = UserManager()

    def __str__(self):
        return self.email


class Vendor(models.Model):
    name = models.CharField(max_length=100)
    purchase_order_number = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=100)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Vehicle(models.Model):
    vehicle_number = models.CharField(max_length=20)
    vehicle_type = models.CharField(max_length=50)
    delivery_challan_number = models.CharField(max_length=50)
    purchase_order_number = models.CharField(max_length=50)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.vehicle_number

class QualityCheck(models.Model):
    vehicle = models.OneToOneField(Vehicle, on_delete=models.CASCADE)
    passed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.vehicle.vehicle_number} - {'Passed' if self.passed else 'Failed'}"

class Checkout(models.Model):
    vehicle = models.OneToOneField(Vehicle, on_delete=models.CASCADE)
    checked_out_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.vehicle.vehicle_number} - Checked Out at {self.checked_out_at}"
