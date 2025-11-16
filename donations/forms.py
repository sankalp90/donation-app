from django import forms
from .models import DonationItem, ItemRequest

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
