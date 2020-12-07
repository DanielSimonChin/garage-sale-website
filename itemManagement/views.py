from django.views import generic
from django.utils import timezone
from django.shortcuts import render , get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from database.models import User,Item,Comment,Reply
from django.shortcuts import redirect
from django.contrib.auth import login, authenticate,logout
from django.contrib.auth.forms import UserChangeForm,PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from .forms import itemCreateForm,UpdateItemForm

# Create your views here.
#The view for the index which contains all the listed items on the site with their title and image
class IndexView(generic.ListView):
    template_name = 'itemManagement/index.html'
    context_object_name = 'item_list'
    
    #return all the items in order of publication date
    def get_queryset(self):
        return Item.objects.order_by('-pub_date')
      
#The view for the detail's page of every item
class DetailView(generic.DetailView):
    model = Item
    template_name = 'itemManagement/detail.html'

    def get_queryset(self):
        #Excludes any items that aren't published yet.
        return Item.objects.filter(pub_date__lte=timezone.now())
    
def createItemView(request):
    form = itemCreateForm()
    if(request.method == 'POST'):
        form = itemCreateForm(request.POST,request.FILES)
        
        if form.is_valid():
            item = form.save(commit=False)
            
            owner = User.objects.filter(email=request.user.email).first()
            item.owner = owner
            item.save()
            
            #form.owner = request.user
            #form.save()
            return redirect('/')
        else:
            return redirect('/create/')
        
    context = {'item_form': form}    
    return render(request,'itemManagement/createItem.html', context)

def updateItem(request, pk):
    item = Item.objects.get(id=pk)
    form = UpdateItemForm(instance=item)
    
    if request.method == 'POST':
        form = UpdateItemForm(request.POST,request.FILES,instance=item)
        
        if form.is_valid():
            form.save()
            return redirect('/')
        
    context = {'item_form': form}   
    return render(request,'itemManagement/updateItem.html', context)

def deleteItem(request,pk):    
    item = Item.objects.get(id=pk)

    if request.method == 'POST':
        item.delete()
        return redirect('/')
    
    context={'item': item}
    return render(request,'itemManagement/delete.html',context)
    
            