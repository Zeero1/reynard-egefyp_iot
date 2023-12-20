from django.db import models
from django.contrib.auth.models import User

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

    def __str__(self):
        return self.user.username
