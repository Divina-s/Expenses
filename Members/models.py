from django.db import models
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


# Create your models here.
class UserPreference(models.Model):
    user=models.OneToOneField(to=User, on_delete=models.CASCADE)
    currency=models.CharField(max_length=55,blank=True, null=True)



    def __str__(self):
        return str(user)+'s'+'preferences'
class UserProfile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE, null=True)  
    bio=models.TextField()
    profile_pic=models.ImageField(null=True, blank="True", upload_to='images/profile')
    
    def __str__(self):
        return str(self.user)