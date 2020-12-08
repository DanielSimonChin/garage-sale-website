from django.views import generic
from django.utils import timezone
from django.shortcuts import render , get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from database.models import User,Item,Comment,Reply
from .forms import CommentForm, ReplyForm
from django.shortcuts import redirect
from django.contrib.auth import login, authenticate,logout
from django.contrib.auth.forms import UserChangeForm,PasswordChangeForm
from django.contrib.auth import update_session_auth_hash

# Create your views here.
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
 
def like(request, pk):
    if not request.user.is_authenticated:
        return redirect("login")
    item = get_object_or_404(Item, id=pk)
    item.likes.add(request.user)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))