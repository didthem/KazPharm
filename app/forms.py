from django.contrib.auth.models import User
from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm
from .models import *


class RegisterUserForm(UserCreationForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': "form-input"}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': "form-input"}))
    username = forms.CharField(widget=forms.TextInput(attrs={"class": "form-input"}))
    email = forms.EmailField(widget=forms.TextInput(attrs={"class": "form-input"}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={"class": "form-input"}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={"class": "form-input"}))
    class Meta:
        model = User
        fields = "username", "email", "password1", "password2" 



class AuthUserForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={"class": "form-input"}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={"class": "form-input"}))


class UserProfileForm(UserChangeForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control py-4', 'readonly': True}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control py-4', 'readonly': True}))
    image = forms.ImageField(widget=forms.FileInput(attrs={'class': 'custom-file-input'}), required=False)
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control py-4'}))
    email = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control py-4'}))
    class Meta:
       model = User
       fields = ('first_name', 'last_name', 'image', 'username', 'email')

class User(models.Model):
  username = models.CharField(max_length=255)
  email = models.EmailField()
  avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)


