from django import forms
from database.models import User,Comment, Reply
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth import authenticate

#The registration form that displays all necessary fields
class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('email','username','first_name','last_name','date_of_birth','password1','password2')

#The account edit form that displays all necessary fields 
class AccountEditForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('avatar','email','username','first_name','last_name','date_of_birth')
        
#The form presented whenever the user clicks on login
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

        
        
        
        
              