from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import DonationItem, ItemRequest
from .forms import DonationItemForm, ItemRequestForm

def home_view(request):
    return render(request, 'donations/home.html')

def map_view(request):
    items = DonationItem.objects.filter(is_claimed=False)
    return render(request, 'donations/map.html', {'items': items})


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
            return redirect('item_detail', item_id=item.id)
    else:
        form = DonationItemForm()
    return render(request, 'donations/item_add.html', {'form': form})


def item_detail(request, item_id):
    item = get_object_or_404(DonationItem, id=item_id)
    return render(request, 'donations/item_detail.html', {'item': item})


@login_required
def request_item(request, item_id):
    item = get_object_or_404(DonationItem, id=item_id)

    if item.is_claimed:
        messages.error(request, "Item already taken.")
        return redirect('item_detail', item_id=item_id)

    if request.method == 'POST':
        form = ItemRequestForm(request.POST)
        if form.is_valid():
            request_entry = form.save(commit=False)
            request_entry.item = item
            request_entry.requester = request.user
            request_entry.save()
            messages.success(request, "Request sent to donor!")
            return redirect('item_detail', item_id=item_id)
    else:
        form = ItemRequestForm()

    return render(request, 'donations/request_item.html',
                  {'form': form, 'item': item})


@login_required
def my_donations(request):
    items = DonationItem.objects.filter(donor=request.user)
    return render(request, 'donations/my_donations.html', {'items': items})


@login_required
def my_requests(request):
    requests = ItemRequest.objects.filter(requester=request.user)
    return render(request, 'donations/my_requests.html', {'requests': requests})
