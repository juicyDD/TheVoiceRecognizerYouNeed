from django import forms 
from django.contrib.auth.models import User 
from django.contrib.auth.forms import UserCreationForm 

class SignUpForm(UserCreationForm): 
    
    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control search-input'
        self.fields['first_name'].widget.attrs.update({ 'placeholder':'First Name', }) 
        self.fields['last_name'].widget.attrs.update({ 'placeholder':'Last name', }) 
        self.fields['username'].widget.attrs.update({ 'placeholder':'Username', }) 
        self.fields['email'].widget.attrs.update({ 'placeholder':'Email', }) 
        self.fields['password1'].widget.attrs.update({ 'placeholder':'Password', }) 
        self.fields['password2'].widget.attrs.update({ 'placeholder':'Confirm password', }) 
    class Meta: 
        model = User 
        fields = ( 'first_name', 'last_name', 'username', 'email', 'password1', 'password2', )