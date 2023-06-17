from django.urls import path
from .views import loginView,registerView, landingView, logoutView, usernameValidationView, emailValidationView, indexView, profileView, UserChangeView,PasswordsChangeView, PasswordSuccessView
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import views as auth_views
urlpatterns = [
    path('SignIn/', loginView.as_view(), name='login'),
    path('register/', registerView.as_view(), name ='register'),
    path('',landingView, name='landing'), 
    path('signout/', logoutView, name ='logout'),
    path('validateusername/',csrf_exempt(usernameValidationView.as_view()), name='validate-username'),
    path('validat<eemail/',csrf_exempt(emailValidationView.as_view()), name='validate-email'),
    path('preferences/', indexView, name ='preferences'),
    path('profile/', profileView.as_view(), name ='profile'),
    path('editprofile/',UserChangeView.as_view(), name ='edit_profile'),
    #path('<int:pk>/password/', auth_views.PasswordChangeView.as_view(template_name='set-newpassword.html')),
    path('<int:pk>/password/',PasswordsChangeView.as_view(template_name='set-newpassword.html'), name='set_password'),
    path('successpassword/' ,PasswordSuccessView, name="password-success")
  
   
]