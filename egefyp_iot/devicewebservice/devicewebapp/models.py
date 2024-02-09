from django.db import models
from django.contrib.auth.models import User

# from rest_framework.authtoken.models import Token 

# Create your models here.
"""
    Users Profile Info Class - inherits from models.Model
    Model class to add additional info that the default model
    does not have (default: username email password first name and
    last name)
"""
class UserProfileInfo(models.Model):

    user = models.OneToOneField(User,on_delete=models.CASCADE,unique=True)
    #def __init__(self):
    #    self.user = user

    #additional classes
    user_site = models.URLField(blank=True)

    # If you've already created some users, you can generate tokens for all existing users like this:
    # for user in User.objects.all():
    #     Token.objects.get_or_create(user=user)
    def __str__(self):
        return self.user.username

class Device(models.Model):
    hostnm = models.CharField(max_length=100)
    ipaddr = models.CharField(max_length=30)
    macaddr = models.CharField(max_length=30)
    isonline = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.hostnm} {self.ipaddr} {self.macaddr}"

