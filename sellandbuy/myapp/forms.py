from django import forms
from .models import Product

from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class user_registeration_form(UserCreationForm) :
    # now this user_registeration_form is just a replica of the real usercreationform since we called it as arg in the brackets
    class Meta :
        model = User
        # now this is why we imported user model from auth
        fields = ['username','first_name','last_name' ,'email', 'password1', 'password2']
    

class Product_form(forms.ModelForm):
    desc = forms.CharField(label='Product description (optional)', required=False, widget=forms.Textarea)

    class Meta:
        model = Product
        fields = ['code','name','desc','seller','price','image_field']