from django.views import generic
from django.utils import timezone
from django.shortcuts import render
from django.http import HttpResponse
from django.urls import reverse
from database.models import User,Item,Comment,Reply
from .forms import RegisterForm
from django.shortcuts import redirect
from django.contrib.auth import login, authenticate,logout



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
    




