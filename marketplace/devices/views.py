from django.shortcuts import render, get_object_or_404, redirect
from .models import Device, Review, Category
from .forms import ReviewForm
from django.contrib.auth.decorators import login_required
from accounts.models import Profile
from django.db import connection


def device_showcase(request):
    devices = Device.objects.all()

    if request.user.is_authenticated:
        profile = Profile.objects.get(user=request.user)
        return render(request, 'devices/device_showcase.html', {'devices': devices, 'profile': profile})
    else:
        return render(request, 'devices/device_showcase.html', {'devices': devices})


def device_detail(request, device_id):
    device = get_object_or_404(Device, pk=device_id)

    if request.user.is_authenticated:
        profile = Profile.objects.get(user=request.user)
        return render(request, 'devices/device_detail.html', {'device': device, 'profile': profile})
    else:
        return render(request, 'devices/device_detail.html', {'device': device})


def create_review(request, device_id):
    device = get_object_or_404(Device, pk=device_id)
    profile = Profile.objects.filter(user=request.user)

    if request.method == 'POST':
        review_form = ReviewForm(request.POST)
        if review_form.is_valid():
            review = review_form.save(commit=False)
            review.author = request.user
            review.device = device
            review.save()
            return redirect('device_detail', device_id=device_id)
    else:
        review_form = ReviewForm()
    return render(request, 'devices/device_detail.html', {'review_form': review_form, 'device': device,
                                                          'profile': profile})


def show_device_reviews(request, device_id):
    reviews = Review.objects.select_related('device', 'author') \
                            .only('device__name', 'author__username', 'rating', 'content') \
                            .filter(device_id=device_id)
    device_name = reviews.first().device.name if reviews.exists() else Device.objects.get(pk=device_id).name

    if request.user.is_authenticated:
        profile = Profile.objects.get(user=request.user)
        return render(request, 'devices/device_reviews.html', {'device_id': device_id,
                                                               'device_name': device_name,
                                                               'reviews': reviews,
                                                               'profile': profile})
    else:
        return render(request, 'devices/device_reviews.html', {'device_id': device_id,
                                                               'device_name': device_name,
                                                               'reviews': reviews})


def show_device_categories(request):
    categories = Category.objects.all()

    if request.user.is_authenticated:
        profile = Profile.objects.get(user=request.user)
        return render(request, 'devices/device_categories.html', {'categories': categories,
                                                                  'profile': profile})

    return render(request, 'devices/device_categories.html', {'categories': categories})


def show_devices_by_category(request, category_id):
    category = get_object_or_404(Category, pk=category_id)
    devices = Device.objects.filter(category=category)

    if request.user.is_authenticated:
        profile = Profile.objects.get(user=request.user)
        return render(request, 'devices/devices_by_category.html', {'category': category,
                                                                    'devices': devices,
                                                                    'profile': profile})

    return render(request, 'devices/devices_by_category.html', {'category': category,
                                                                'devices': devices})


