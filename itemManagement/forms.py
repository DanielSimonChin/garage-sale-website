from django import forms
from database.models import Item

#The form which appears when a user creates a new item. Display all necessary fields that are not defaulted
class itemCreateForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ('image','title','description','price')
        widgets = {
            'description' : forms.Textarea(attrs={'class':'form-control'}),
        }

#The form which appears when a user updates an item. Display all necessary fields that are not defaulted
class UpdateItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ('image','title','description','price')
        widgets = {
            'description' : forms.Textarea(attrs={'class':'form-control'}),
        }