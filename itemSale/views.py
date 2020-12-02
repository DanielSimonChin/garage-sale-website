from django.views import generic
from django.utils import timezone
from django.shortcuts import render
from django.http import HttpResponse
from django.urls import reverse
from .models import User,Item,Comment,Reply

# Create your views here.

class IndexView(generic.ListView):
    template_name = 'itemSale/index.html'
    context_object_name = 'item_list'
    
    def get_queryset(self):
        return Item.objects.order_by('-pub_date')
        
class DetailView(generic.DetailView):
    model = Item
    template_name = 'itemSale/detail.html'

    def get_queryset(self):
        #Excludes any items that aren't published yet.
        return Item.objects.filter(pub_date__lte=timezone.now())