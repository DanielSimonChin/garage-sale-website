from django.views import generic
from django.utils import timezone
from django.shortcuts import render
from django.http import HttpResponse
from django.urls import reverse
from database.models import User,Item,Comment,Reply
from .forms import RegisterForm,UserAuthenticationForm,AccountEditForm
from django.shortcuts import redirect
from django.contrib.auth import login, authenticate,logout
from django.contrib.auth.forms import UserChangeForm


#The view for the index which contains all the listed items on the site with their title and image
class IndexView(generic.ListView):
    template_name = 'authentication/index.html'
    context_object_name = 'item_list'
    
    #return all the items in order of publication date
    def get_queryset(self):
        return Item.objects.order_by('-pub_date')
      
#The view for the detail's page of every item
class DetailView(generic.DetailView):
    model = Item
    template_name = 'authentication/detail.html'

    def get_queryset(self):
        #Excludes any items that aren't published yet.
        return Item.objects.filter(pub_date__lte=timezone.now())

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
            return redirect('/authentication/')
        else:
            context['registration_form'] = form
    #
    else:
        form = RegisterForm()
        context['registration_form'] = form
		
    
    return render(request,'authentication/register.html', context)


def logout_view(request):
    logout(request)
    return redirect('/authentication/')


def login_view(request):
    context = {}
    user = request.user
    
    if user.is_authenticated:
        return redirect('/authentication/')
    
    if request.POST:
        form = UserAuthenticationForm(request.POST)
        
        if form.is_valid():
            email = request.POST['email']
            password = request.POST['password']
            user = authenticate(email=email,password=password)
            
            if user:
                login(request,user)
                return redirect('/authentication/')
    else:
        form = UserAuthenticationForm()
        
    context['loginForm'] = form
    return render(request,'authentication/login.html', context)

# def account_view(request):
#     if not request.user.is_authenticated:
#         return redirect('authentication/login.html')
    
#     context = {}
#     if request.POST:
#         form = AccontUpdateForm(request.POST, instance=request.user)
#         if form.is_valid():
#             form.save()
#     else:
#         form = AccontUpdateForm(initial = {"email": request.user.email,"username": request.user.username,"first_name": request.user.first_name,"last_name": request.user.last_name,"date_of_birth":request.user.date_of_birth})
    
#     context['account_form'] = form
#     return render(request,'authentication/account.html',context)

def account_view(request):
    context = {}
    if(request.method == 'POST'):
        form = AccountEditForm(request.POST,instance=request.user)
        
        if form.is_valid():
            #make the changes to the user
            form.save()
            
            return redirect('/authentication/')
    else:
        form = AccountEditForm(instance = request.user)
        context['account_form'] = form
		
    return render(request,'authentication/account.html', context)



