from django import forms
from database.models import User,Comment, Reply
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth import authenticate

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ( 'text',)
        widgets = {
            'text' : forms.Textarea(attrs={'class':'form-control'}),
        }
        
class ReplyForm(forms.ModelForm):
    class Meta:
        model = Reply
        fields = ( 'text',)
        widgets = {
            'text' : forms.Textarea(attrs={'class':'form-control'}),
        }