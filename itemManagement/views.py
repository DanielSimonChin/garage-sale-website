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
from django.db.models import Count
from django.contrib import messages

#The view for the index which contains all the listed items on the site with their title and image
class IndexView(generic.ListView):
    template_name = 'itemManagement/index.html'
    context_object_name = 'item_list'
    
    #return all the items in order of publication date
    def get_queryset(self):
        filter = self.request.GET.get('filter')
        userSearch = self.request.GET.get('search')
        
        #filter the index list depending on the selected filter choice.
        if filter == 'recent':
            qs = Item.objects.order_by('-pub_date')
        elif filter == 'oldest':
            qs = Item.objects.order_by('pub_date')
        elif filter == 'popular':
            stringFilter = 'total_likes'
            qs = Item.objects.annotate(like_count=Count('likes')).order_by('-like_count')
        elif filter == 'liked':
            user = self.request.user
            qs = Item.objects.filter(likes = user)
        elif filter == 'owned':
            user = self.request.user
            qs = Item.objects.filter(owner = user)
        else:
            qs = Item.objects.order_by('-pub_date')
            
            
        if userSearch:
            if len(userSearch) != 0:
                qs = qs.filter(title__contains=userSearch)
        
        return qs
        
      
#The view for the detail's page of every item
class DetailView(generic.DetailView):
    model = Item
    template_name = 'itemManagement/detail.html'

    def get_queryset(self):
        #Excludes any items that aren't published yet.
        return Item.objects.filter(pub_date__lte=timezone.now())

#The view that appears whenever a user clicks on Sell item
def createItemView(request):
    if not request.user.is_authenticated:
        return redirect("login")
    
    form = itemCreateForm()
    if(request.method == 'POST'):
        form = itemCreateForm(request.POST,request.FILES)
        
        #If the form is valid, save it to the db
        if form.is_valid():
            item = form.save(commit=False)
            
            owner = User.objects.filter(email=request.user.email).first()
            item.owner = owner
            item.save()
            
            #return to home page
            return redirect('/')
        else:
            return redirect('/create/')
        
    context = {'item_form': form}    
    return render(request,'itemManagement/createItem.html', context)

#The view for updating an existing item
def updateItem(request, pk):
    if not request.user.is_authenticated:
        return redirect("login")
    
    #get the selected item to update 
    item = Item.objects.get(id=pk)
    form = UpdateItemForm(instance=item)
    
    if request.method == 'POST':
        form = UpdateItemForm(request.POST,request.FILES,instance=item)
        
        if form.is_valid():
            #save the item changes and return to home page
            form.save()
            return redirect('/')
        
    context = {'item_form': form}   
    return render(request,'itemManagement/updateItem.html', context)

#The view for whenever a user wants to delete an item. Confirms if they wish to continue
def deleteItem(request,pk):    
    if not request.user.is_authenticated:
        return redirect("login")
    
    item = Item.objects.get(id=pk)

    if request.method == 'POST':
        #delete the selected item and return to home page.
        item.delete()
        return redirect('/')
    
    context={'item': item}
    return render(request,'itemManagement/delete.html',context)
    
#The function which processes a user's request to buy an item. Calculates if they have sufficient funds.
def buyItem(request,pk):
    if not request.user.is_authenticated:
        return redirect("login")
    
    item = Item.objects.get(id=pk)
    
    buyer = request.user
    if buyer.balance >= item.price:
        #new owner's balance decreases since they bought a new item
        buyer.balance = buyer.balance - item.price
        
        #The original owner's balance increases by the item's cost
        oldOwner = item.owner
        oldOwner.balance = oldOwner.balance + item.price
        
        #transfer ownership to the new owner of the item
        item.owner = buyer
        
        #save the changes to the db
        buyer.save()
        oldOwner.save()
        item.save()
        
    else:
        context = {}
        return render(request,'itemManagement/missingFunds.html',context)
    
    #return to the currently viewed item
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))