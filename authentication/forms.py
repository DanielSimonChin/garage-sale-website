# -*- coding: utf-8 -*-
"""
Created on Wed Dec  2 22:04:50 2020

@author: Daniel
"""
from django import forms
#from django.contrib.auth.models import User
from database.models import User,Comment, Reply
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

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ( 'text',)
        widgets = {
            'text' : forms.Textarea(attrs={'class':'form-control'}),
        }
        
class ReplyForm(forms.ModelForm):
    class Meta:
        model = Reply
        fields = ( 'text',)
        widgets = {
            'text' : forms.Textarea(attrs={'class':'form-control'}),
        }
        
        
        
        
              