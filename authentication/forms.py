# -*- coding: utf-8 -*-
"""
Created on Wed Dec  2 22:04:50 2020

@author: Daniel
"""
from django import forms
#from django.contrib.auth.models import User
from database.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth import authenticate

class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('email','username','first_name','last_name','date_of_birth','password1','password2')
        
class AccountEditForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('email','username','first_name','last_name','date_of_birth')
        

class UserAuthenticationForm(forms.ModelForm):
    password = forms.CharField(label="Password",widget=forms.PasswordInput())
    
    class Meta:
        model = User
        fields = ('email','password')
		
    def clean(self):
        email = self.cleaned_data['email']
        password = self.cleaned_data['password']
        if not authenticate(email = email, password = password):
            raise forms.ValidationError("Invalid login!")
        
# class AccontUpdateForm(forms.ModelForm):
#         class Meta:
#             model = User
#             fields = ('email','username','first_name','last_name','date_of_birth')
            
#         def clean_email(self):
#             if self.is_valid():
#                 email = self.cleaned_data['email']
#                 try:
#                     userAccount = User.objects.exclude(pk=self.instance.pk).get(email=email)
#                 except User.DoesNotExist:
#                     return email
#                 raise forms.ValidationError('This email is already taken :', userAccount.email)
                
#         def clean_username(self):
#             if self.is_valid():
#                 username = self.cleaned_data['username']
#                 try:
#                     userAccount = User.objects.exclude(pk=self.instance.pk).get(username=username)
#                 except User.DoesNotExist:
#                     return username
#                 raise forms.ValidationError('This username is already taken :', userAccount.username)
        
#         def clean_first_name(self):
#             if self.is_valid():
#                 first_name = self.cleaned_data['first_name']
#                 return first_name
#         def clean_last_name(self):
#             if self.is_valid():
#                 last_name = self.cleaned_data['last_name']
#                 return last_name
#         def clean_dob(self):
#             if self.is_valid():
#                 date_of_birth = self.cleaned_data['date_of_birth']
#                 return date_of_birth
                
    