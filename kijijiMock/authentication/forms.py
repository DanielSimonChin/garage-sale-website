# -*- coding: utf-8 -*-
"""
Created on Wed Dec  2 22:04:50 2020

@author: Daniel
"""
from django import forms
#from django.contrib.auth.models import User
from database.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate

class RegisterForm(UserCreationForm):
    #email = forms.EmailField(verbose_name='email',max_length=60, unique=True)
    class Meta:
        model = User
        fields = ('email','username','first_name','last_name','date_of_birth','password1','password2')
        

class UserAuthenticationForm(forms.ModelForm):
    password = forms.CharField(label="Password",widget=forms.PasswordInput())
		
    
        
        