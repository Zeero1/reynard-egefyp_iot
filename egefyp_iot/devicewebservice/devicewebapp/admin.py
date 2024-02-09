from django.contrib import admin
from devicewebapp.models import UserProfileInfo, Device

# Register your models here.
admin.site.register(UserProfileInfo, Device)
