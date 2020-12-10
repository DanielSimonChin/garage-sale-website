from django.views import generic
from django.utils import timezone
from django.shortcuts import render , get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from database.models import User,Item,Comment,Reply
from .forms import RegisterForm,UserAuthenticationForm,AccountEditForm
from django.shortcuts import redirect
from django.contrib.auth import login, authenticate,logout
from django.contrib.auth.forms import UserChangeForm,PasswordChangeForm
from django.contrib.auth import update_session_auth_hash


#Function view for whenever the user clicks on Register nav item.
def register(request):
    context = {}
    if(request.method == 'POST'):
        form = RegisterForm(request.POST)
        
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email')
            raw_password = form.cleaned_data.get('password1')
            #create the account using the input email and password
            account = authenticate(email=email,password=raw_password)
            #login to the recently created account
            login(request,account)
            return redirect('/')
        else:
            context['registration_form'] = form
    #If it is a GET request
    else:
        form = RegisterForm()
        context['registration_form'] = form
		
    #display the html with the form
    return render(request,'authentication/register.html', context)


#Logout of the authenticated account
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

#The view for whenever the user clicks on the login button
def login_view(request):
    context = {}
    user = request.user
    
    #bring the user to the home page if authenticated
    if user.is_authenticated:
        return redirect('/')
    
    if request.POST:
        form = UserAuthenticationForm(request.POST)
        
        if form.is_valid():
            email = request.POST['email']
            password = request.POST['password']
            #login the user with the credentials
            user = authenticate(email=email,password=password)
            
            if user:
                #if the credentials are valid, bring login and bring them back to home
                login(request,user)
                return redirect('/')
    else:
        form = UserAuthenticationForm()
        
    context['loginForm'] = form
    return render(request,'authentication/login.html', context)
 
   
#The view for a user to edit his or her account
def account_view(request):
    if not request.user.is_authenticated:
        return redirect("login")
    
    context = {}
    if(request.method == 'POST'):
        form = AccountEditForm(request.POST,request.FILES,instance=request.user)
        
        if form.is_valid():
            #make the changes to the user
            form.save()
            
            return redirect('/')
    else:
        form = AccountEditForm(instance = request.user)
        context['account_form'] = form
		
    return render(request,'authentication/account.html', context)

#The view for a user to edit his or her password
def password_view(request):
    if not request.user.is_authenticated:
        return redirect("login")
    
    context = {}
    if(request.method == 'POST'):
        form = PasswordChangeForm(data=request.POST,user=request.user)
        
        if form.is_valid():
            #make the changes to the user
            form.save()
            update_session_auth_hash(request, form.user)
            
            return redirect('/')
        else:
            #keep them at the password form if the password entered is invalid
            return redirect('/password/')
    else:
        form = PasswordChangeForm(user = request.user)
        context['password_form'] = form
		
    return render(request,'authentication/password_change.html', context)

