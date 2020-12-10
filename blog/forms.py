from django import forms
from database.models import User,Comment, Reply
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth import authenticate

#The form that appears when a user clicks on comment. Only need a text field for a new comment
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ( 'text',)
        widgets = {
            'text' : forms.Textarea(attrs={'class':'form-control'}),
        }

#The form for whenever the user clicks on reply to a comment. Only need a text field for the reply
class ReplyForm(forms.ModelForm):
    class Meta:
        model = Reply
        fields = ( 'text',)
        widgets = {
            'text' : forms.Textarea(attrs={'class':'form-control'}),
        }