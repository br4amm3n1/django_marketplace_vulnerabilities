from django.contrib import admin
from .models import Cart, CartItem, Purchase

# Register your models here.
admin.site.register([Cart, CartItem, Purchase])
