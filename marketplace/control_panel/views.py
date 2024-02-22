from django.shortcuts import render
from accounts.models import Profile, Transaction
from devices.models import Review
from cart.models import Purchase
from django.contrib.auth.decorators import login_required
from .logic import *
from django.db.models import Q
import json


# Create your views here.
@login_required
@check_group(group_name='moderator')
def view_capabilities(request):
    profile = Profile.objects.get(user=request.user)

    ccf_warning_message = None

    remove_category_form = remove_category(request)
    create_category_context = create_category(request)
    add_device_form = add_device(request)

    if create_category_context['warning_message'] is not None:
        ccf_warning_message = create_category_context['warning_message']

    return render(request, 'control_panel/main_page.html', {'profile': profile,
                                                            'create_category_form': create_category_context['create_form'],
                                                            'ccf_warning_message': ccf_warning_message,
                                                            'remove_category_form': remove_category_form,
                                                            'add_device_form': add_device_form})


@login_required
@check_group(group_name='moderator')
def view_reviews(request):
    profile = Profile.objects.get(user=request.user)
    keyword = request.GET.get('keyword', '')

    reviews = Review.objects.select_related('author', 'device') \
                            .only('id', 'device__name', 'content', 'rating',
                                  'author__username') \
                            .filter(Q(content__icontains=keyword) | Q(device__name__icontains=keyword) |
                                    Q(author__username__icontains=keyword)) \
                            .all()

    remove_review(request)

    return render(request, 'control_panel/list_reviews.html', {'profile': profile, 'reviews': reviews,
                                                               'keyword': keyword})


@login_required
@check_group(group_name='moderator')
def view_purchases(request):
    profile = Profile.objects.get(user=request.user)

    purchases = Purchase.objects.select_related('user').all()

    purchases_data = []

    for purchase in purchases:
        devices_data = json.loads(purchase.purchased_devices)
        purchases_data.append({
            'user': purchase.user.username,
            'delivery_address': purchase.delivery_address,
            'timestamp': purchase.timestamp,
            'amount': purchase.amount,
            'devices': devices_data
        })

    return render(request, 'control_panel/list_purchases.html', {'profile': profile,
                                                                 'purchases': purchases_data})


@login_required
@check_group(group_name='moderator')
def view_transactions(request):
    profile = Profile.objects.get(user=request.user)
    keyword = request.GET.get('keyword', '')

    transactions = Transaction.objects.select_related('user') \
                                      .filter(Q(card_number__icontains=keyword) | Q(card_holder__icontains=keyword) |
                                              Q(user__username__icontains=keyword) | Q(timestamp__icontains=keyword)) \
                                      .all()

    return render(request, 'control_panel/list_transactions.html', {'profile': profile,
                                                                    'transactions': transactions})

