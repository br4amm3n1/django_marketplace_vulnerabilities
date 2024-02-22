from django.urls import path
from . import views

urlpatterns = [
    path('', views.cart_view, name='cart'),
    path('add_to_cart/<int:device_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove_from_cart/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('purchase/', views.make_a_purchase, name='make_purchase'),
    path('purchase/dadata_autocomplete/', views.dadata_autocomplete, name='dadata_autocomplete'),
]
