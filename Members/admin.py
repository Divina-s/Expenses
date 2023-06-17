from django.contrib import admin
from .models import UserPreference, UserProfile
# Register your models here.
class UserPreferenceAdmin(admin.ModelAdmin):
    list_display=('user','currency')
   
admin.site.register(UserPreference,UserPreferenceAdmin)





admin.site.register(UserProfile)
