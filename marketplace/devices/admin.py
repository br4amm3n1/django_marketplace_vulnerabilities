from django.contrib import admin
from .models import Category, Device, Review

# Register your models here.
admin.site.register([Category, Device, Review])
