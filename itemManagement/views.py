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
from .forms import itemCreateForm

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
    context = {}
    if(request.method == 'POST'):
        form = itemCreateForm(request.POST,instance=request.user)
        
        if form.is_valid():
            user = User.objects.get(pk=request.user.pk)
            title = request.POST.get('title')
            image = request.POST.get('image')
            description = request.POST.get('description')
            price = request.POST.get('price')
            
            item = Item.objects.create(user=user,title=title,image=image,price=price,description=description)

            if item:
                item.save()
                return redirect('/')
    else:
        form = itemCreateForm()
        context['item_form'] = form
		
    return render(request,'itemManagement/createItem.html', context)