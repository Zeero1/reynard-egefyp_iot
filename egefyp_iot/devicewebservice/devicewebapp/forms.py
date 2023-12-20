from django import forms
from django.contrib.auth.models import User
from devicewebapp.models import UserProfileInfo

class UserForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
            'placeholder':'Username Required',
            'title':'Username Required, only letters,numbers and @,.,+,-,_',
            'required':'true',
            'width':'300',
            }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
            'placeholder':'Password Required',
            'required':'true',
            'width':'300',
            }))

    class Meta():
        model = User
        fields = ('username','email','password')

class UserProfileInfoForm(forms.ModelForm):
    class Meta():
        model = UserProfileInfo
        fields = ('user_site',)
