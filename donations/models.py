from django.db import models
from django.contrib.auth.models import User

class DonationItem(models.Model):
    CATEGORY_CHOICES = [
        ('clothes', 'Clothes'),
        ('books', 'Books'),
        ('food', 'Food'),
        ('electronics', 'Electronics'),
        ('furniture', 'Furniture'),
        ('other', 'Other'),
    ]

    donor = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    category = models.CharField(max_length=30, choices=CATEGORY_CHOICES)
    image = models.ImageField(upload_to="items/", blank=True, null=True)
    latitude = models.FloatField()
    longitude = models.FloatField()
    condition = models.CharField(max_length=30, default="Good")
    is_claimed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class ItemRequest(models.Model):
    item = models.ForeignKey(DonationItem, on_delete=models.CASCADE)
    requester = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField(blank=True)
    approved = models.BooleanField(default=False)
    requested_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.requester} → {self.item}"
