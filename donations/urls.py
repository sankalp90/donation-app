from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'), 
    path('map/', views.map_view, name='donation_map'), 
    path('items/', views.item_list, name='item_list'),
    path('items/<int:pk>/', views.item_detail, name='item_detail'),
    path('items/add/', views.item_add, name='item_add'),
    path('my-donations/', views.my_donations, name='my_donations'),
    path('my-requests/', views.my_requests, name='my_requests'),
]
