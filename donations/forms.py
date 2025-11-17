from django import forms
from .models import DonationItem, ItemRequest
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class DonationItemForm(forms.ModelForm):
    class Meta:
        model = DonationItem
        fields = [
            'title', 'description', 'category', 'condition',
            'image', 'latitude', 'longitude'
        ]


class ItemRequestForm(forms.ModelForm):
    class Meta:
        model = ItemRequest
        fields = ['message']
        widgets = {
            'message': forms.Textarea(attrs={
                'class': 'border rounded w-full p-2',
                'placeholder': 'Write a message to the donor...',
                'rows': 4
            }),
        }

class SignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
