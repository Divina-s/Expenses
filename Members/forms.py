
from django.contrib.auth.models import User
from django import forms
from django.contrib.auth.forms import UserCreationForm,  UserChangeForm, PasswordChangeForm

class EditProfileForm(UserChangeForm):
     def __init__(self, *args, **kwargs):
       super().__init__(*args, **kwargs) 
       self.fields["first_name"].widget.attrs.update ({
          'required':'',
          'name':"first_name",
          'id':"first_name",
          'type':'text',
          'class':"form-control",
          'placeholder':"",
          'max-length':'22',
          'minlength':"3",
       })
       self.fields["last_name"].widget.attrs.update ({
          'required':'',
          'name':"last_name",
          'id':"last_name",
          'type':'text',
          'class':"form-control",
          'placeholder':"",
          'max-length':'22',
          'minlength':"3",
       })
       self.fields["username"].widget.attrs.update ({
          'required':'',
          'name':"username",
          'id':"username",
          'type':'text',
          'class':"form-control",
          'placeholder':"Enter username",
          'max-length':'16',
          'minlength':"4",
       })
       self.fields["email"].widget.attrs.update ({
          'required':'',
          'name':"email",
          'id':"email",
          'type':'email',
          'class':"form-control",
          'placeholder':"Enter email",
          
       })
      
     class Meta:
          model=User
          fields=['first_name','last_name', 'username', 'email']
          help_texts={
              'username':None,
          }
class PasswordChangingForm(PasswordChangeForm):
     def __init__(self, *args, **kwargs):
       super().__init__(*args, **kwargs) 
       self.fields["old_password"].widget.attrs.update ({
          'required':'',
          'name':"old_password",
          'id':"old_password",
          'type':'text',
          'class':"form-control",
          'max-length':'22',
          'minlength':"4",
         })
       self.fields["new_password1"].widget.attrs.update ({
          'required':'',
          'name':"new_password1",
          'id':"new_password1",
          'type':'new_password1',
          'class':"form-control",
          ' max-length':'22',
          'minlength':"4",
          
       })
       self.fields["new_password2"].widget.attrs.update ({
          'required':'',
          'name':"new_password2",
          'id':"new_password2",
          'type':'new_password2',
          'class':"form-control",
          ' max-length':'22',
          'minlength':"4",
          
       })