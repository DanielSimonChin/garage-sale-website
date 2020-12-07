from django.views import generic
from django.utils import timezone
from django.shortcuts import render , get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from database.models import User,Item,Comment,Reply
from .forms import RegisterForm,UserAuthenticationForm,AccountEditForm, CommentForm, ReplyForm
from django.shortcuts import redirect
from django.contrib.auth import login, authenticate,logout
from django.contrib.auth.forms import UserChangeForm,PasswordChangeForm
from django.contrib.auth import update_session_auth_hash

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
        

def comment(request, pk):
    if not request.user.is_authenticated:
        return redirect("login")
    
    context = {}
    form = CommentForm(request.POST, instance=request.user)
    
    if form.is_valid():
        text = request.POST.get('text')
        item = Item.objects.get(id = pk)
        comment = Comment.objects.create(item = item,author=request.user,text=text)
        if comment:
            comment.save()
            redirectString = '/' + str(pk) + '/' 
            return redirect(redirectString)
        
        
    context['comment_form'] = form
    
    return render(request, 'authentication/comment.html', context)
    
def reply(request, pk):
    if not request.user.is_authenticated:
        return redirect("login")
    
    context = {}
    form = ReplyForm(request.POST, instance=request.user)
    
    if form.is_valid():
        text = request.POST.get('text')
        comment = Comment.objects.get(id = pk)
        item = Item.objects.get(comments = comment)
        reply = Reply.objects.create(comment = comment,author=request.user,text=text)
        if reply:
            reply.save()
            redirectString = '/' + str(item.id) + '/'
            return redirect(redirectString)
        
        
    context['reply_form'] = form
    
    return render(request, 'authentication/reply.html', context)
    
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
    #
    else:
        form = RegisterForm()
        context['registration_form'] = form
		
    
    return render(request,'authentication/register.html', context)

def like(request, pk):
    if not request.user.is_authenticated:
        return redirect("login")
    item = get_object_or_404(Item, id=pk)
    item.likes.add(request.user)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def login_view(request):
    context = {}
    user = request.user
    
    if user.is_authenticated:
        return redirect('/')
    
    if request.POST:
        form = UserAuthenticationForm(request.POST)
        
        if form.is_valid():
            email = request.POST['email']
            password = request.POST['password']
            user = authenticate(email=email,password=password)
            
            if user:
                login(request,user)
                return redirect('/')
    else:
        form = UserAuthenticationForm()
        
    context['loginForm'] = form
    return render(request,'authentication/login.html', context)
 
   

def account_view(request):
    context = {}
    if(request.method == 'POST'):
        form = AccountEditForm(request.POST,instance=request.user)
        
        if form.is_valid():
            #make the changes to the user
            form.save()
            
            return redirect('/')
    else:
        form = AccountEditForm(instance = request.user)
        context['account_form'] = form
		
    return render(request,'authentication/account.html', context)

def password_view(request):
    context = {}
    if(request.method == 'POST'):
        form = PasswordChangeForm(data=request.POST,user=request.user)
        
        if form.is_valid():
            #make the changes to the user
            form.save()
            update_session_auth_hash(request, form.user)
            
            return redirect('/')
        else:
            return redirect('/password/')
    else:
        form = PasswordChangeForm(user = request.user)
        context['password_form'] = form
		
    return render(request,'authentication/password_change.html', context)

