from django import forms
from .models import Category, foodItem
from accounts.validators import allow_only_images_validator

class categoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['category_name', 'description']
        
class foodItemForm(forms.ModelForm):
    image = forms.FileField(widget=forms.FileInput(attrs={'class': 'btn btn-info w-100'}), validators=[allow_only_images_validator])
    class Meta:
        model = foodItem
        fields = ['category','food_title' ,'description' ,'price' ,'image' ,'is_availabe']
        