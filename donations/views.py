from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import DonationItem, ItemRequest
from .forms import DonationItemForm, ItemRequestForm
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.contrib import messages

def home_view(request):
    return render(request, 'donations/home.html')

def map_view(request):
    items = DonationItem.objects.filter(is_claimed=False)

    items_data = []
    for item in items:
        items_data.append({
            "id": item.id,
            "title": item.title,
            "category": item.get_category_display(),
            "condition": item.condition,
            "donor_username": item.donor.username,
            "latitude": item.latitude,
            "longitude": item.longitude,
            "is_claimed": item.is_claimed,
            "image": item.image.url if item.image else None,
        })

    return render(request, "donations/map.html", {"items": items_data})


def item_list(request):
    items = DonationItem.objects.filter(is_claimed=False)
    return render(request, 'donations/item_list.html', {'items': items})


@login_required
def item_add(request):
    if request.method == 'POST':
        form = DonationItemForm(request.POST, request.FILES)
        if form.is_valid():
            item = form.save(commit=False)
            item.donor = request.user
            item.save()
            messages.success(request, "Item added successfully!")
            return redirect('item_detail', pk=item.id)
    else:
        form = DonationItemForm()
    return render(request, 'donations/item_add.html', {'form': form})


def item_detail(request, pk):
    item = get_object_or_404(DonationItem, id=pk)
    
    if request.user.is_authenticated:
        form = ItemRequestForm()
    else:
        form = None

    return render(request, 'donations/item_detail.html', {'item': item, 'form': form})


@login_required
def request_item(request, pk):
    item = get_object_or_404(DonationItem, id=pk)

    if item.is_claimed:
        messages.error(request, "Item already claimed.")
        return redirect('item_list')

    if request.method == 'POST':
        form = ItemRequestForm(request.POST)
        if form.is_valid():
            item_request = form.save(commit=False)
            item_request.item = item
            item_request.requester = request.user
            item_request.save()
            messages.success(request, "Request sent successfully!")
            return redirect('item_detail', pk=item.id)
    else:
        form = ItemRequestForm()

    return render(request, 'donations/request_item_form.html', {'form': form, 'item': item})



@login_required
def my_donations(request):
    items = DonationItem.objects.filter(donor=request.user)
    return render(request, 'donations/my_donations.html', {'items': items})


@login_required
def my_requests(request):
    requests = ItemRequest.objects.filter(requester=request.user)
    return render(request, 'donations/my_requests.html', {'requests': requests})

def custom_logout(request):
    logout(request) 
    messages.success(request, "You have been logged out successfully!")
    return redirect('home')

from django.contrib.auth import login
from .forms import SignupForm

def signup_view(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Auto login after register
            messages.success(request, "Account created successfully!")
            return redirect('home')
    else:
        form = SignupForm()

    return render(request, "donations/signup.html", {"form": form})


