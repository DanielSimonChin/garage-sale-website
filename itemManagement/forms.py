from django import forms
from database.models import Item

class itemCreateForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ('image','title','description','price')
        widgets = {
            'description' : forms.Textarea(attrs={'class':'form-control'}),
        }

class UpdateItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ('image','title','description','price')
        widgets = {
            'description' : forms.Textarea(attrs={'class':'form-control'}),
        }