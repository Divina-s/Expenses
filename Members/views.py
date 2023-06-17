from typing import Any, Optional
from django.db import models
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm, UserChangeForm ,PasswordChangeForm
from .forms import EditProfileForm, UserCreationForm,PasswordChangingForm
from django.views import View
import json
from django.http import JsonResponse
from django.contrib.auth.models import User
from validate_email import validate_email
from django.contrib import auth
from django.core.mail import EmailMessage
import os
from django.conf import settings
from .models import UserPreference
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.views import PasswordChangeView
class loginView(View):
   def get(self,request):
        return render(request,'login.html',{}) 

   def post(self,request):
      username=request.POST['username']
      password=request.POST['password']

      if username and password:
         user=auth.authenticate(username=username, password=password)

         if user:
            if user.is_active:
               auth.login(request,user)
               messages.success(request,'Welcome, '+user.username+'')
               return redirect('home')
            else:
               messages.error(request, 'You were unable to log in')
               return render(request,'login.html', {})
         else:
          messages.error(request, 'Invalid credentials, try agan')
          return render(request,'login.html', {})
      else:
       messages.error(request, 'Please fill all fields')
       return render(request,'login.html',{})
    
class usernameValidationView(View):
    def post(self,request):
      data=json.loads(request.body)
      username=data['username']
      if User.objects.filter(username=username).exists():
        return JsonResponse({'username_error':'Sorry username is already in use'}, status=409)
        return JsonResponse({'username_valid': True})   
      if not str(username).isalnum():
          return JsonResponse({'username_error':'username should only contain alphanumeric characters'}, status=400)
      return JsonResponse({'username_valid': True})   
    
    
class emailValidationView(View):
    def post(self,request):
      data=json.loads(request.body)
      email=data['email']
      if User.objects.filter(email=email).exists():
        return JsonResponse({'email_error':'Sorry email is already in use'}, status=409)
        return JsonResponse({'email_valid': True})   
      if not validate_email(email) :
          return JsonResponse({'email_error':'email is invalid'}, status=400)
      return JsonResponse({'email_valid': True})             

class registerView(View):
    def get(self,request):
        return render(request,'register.html',{})    
    def post(self,request):
        username=request.POST['username']
        email=request.POST['email']
        password=request.POST['password']

        context={
           'fieldValues': request.POST
        }

        if not User.objects.filter(username=username).exists():
           if not User.objects.filter(email=email).exists():
              
              if len(password) < 6:
                 messages.error(request,'Password too short')
                 return render(request,'register.html',context)  
              user=User.objects.create_user(username=username, email=email)
              user.set_password(password)
              user.save()
              messages.success(request,'Account Successfully created')
              return render(request,'home.html',{} )
       
        return render(request,'home.html',{})  
def landingView(request, *args, **kwargs):
    return render(request, 'landing.html', {})
def logoutView(request):
      logout(request)
      messages.success(request, 'You have been logged out')
      return redirect('login')
def indexView(request):
   currency_data=[]
   file_path=os.path.join(settings.BASE_DIR, 'currencies.json')

   with open(file_path,'r') as json_file:
        
          data=json.load(json_file)
          for k,v in data.items():
           currency_data.append({'name':k, 'value':v})
   
   exists=UserPreference.objects.filter(user=request.user).exists()
   user_preferences=None
   
   if exists:
   
         user_preferences=UserPreference.objects.get(user=request.user)
   
   if request.method=='GET':
     
      return render(request,'preferences/index.html', {'currencies':currency_data, 'user_preferences':user_preferences})
   else:
        currency=request.POST['currency']
        if exists:
             
            
             user_preferences.currency=currency
             user_preferences.save()
        else:     
            UserPreference.objects.create(user=request.user,currency=currency)      
        messages.success(request,'Changes saved')
        return render(request,'preferences/index.html', {'currencies':currency_data, 'user_preferences':user_preferences})

class profileView(View):
   def get(self,request):
        return render(request,'profile.html',{}) 

class UserChangeView(generic.UpdateView):
 
   form_class=EditProfileForm
   template_name='edit_profile.html'
  
   success_url=reverse_lazy('home')


   def get_object(self):
      return self.request.user
   
class PasswordsChangeView(PasswordChangeView):
   form_class=PasswordChangingForm
   success_url=reverse_lazy('password-success')
def PasswordSuccessView(request):
   messages.success(request,'Changes saved')
   return redirect('edit_profile')