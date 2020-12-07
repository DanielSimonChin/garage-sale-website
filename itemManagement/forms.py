from django import forms
from database.models import Item

class itemCreateForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ('image','title','description','price')
        
class UpdateItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ('image','title','description','price')
        
    """ def save(self, commit=True):
        item = self.instance
        item.title = self.cleaned_data['title']
        item.description = self.cleaned_data['description']
        item.price = self.cleaned_data['price']
        
        if self.cleaned_data['image']:
            item.image = self.cleaned_data['image']
        if commit:
            item.save()
        return item """