from django.shortcuts import redirect, render, get_object_or_404
from devices.models import Device
from accounts.models import Profile
from .models import Cart, CartItem
from .forms import PurchaseForm
from django.contrib.auth.decorators import login_required, permission_required
from django.db.models import Prefetch, Sum
from django.contrib.auth.models import User
import json
from dadata import Dadata
from django.conf import settings
from django.http import JsonResponse


# Create your views here.
@login_required
@permission_required('cart.add_cartitem', raise_exception=True)
def add_to_cart(request, device_id):
    device = Device.objects.get(pk=device_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, device=device)

    if not created:
        cart_item.quantity += 1
        cart_item.save()

    return redirect('device_showcase')


@login_required
@permission_required('cart.view_cartitem', raise_exception=True)
def cart_view(request):
    cart, created = Cart.objects.get_or_create(user=request.user)

    cart_items = CartItem.objects.filter(cart=cart).prefetch_related(
        Prefetch('device', queryset=Device.objects.all()),
        Prefetch('cart__user', queryset=User.objects.all())
    )

    profile = Profile.objects.get(user=request.user)

    total_price = cart_items.aggregate(total_price=Sum('device__price'))['total_price'] or 0

    return render(request, 'cart/cart.html',
                      {'cart_items': cart_items, 'total_price': total_price, 'profile': profile})


@login_required
@permission_required('cart.delete_cartitem', raise_exception=True)
def remove_from_cart(request, item_id):
    item = get_object_or_404(CartItem, pk=item_id, cart__user=request.user)
    item.delete()
    return redirect('cart')


@login_required
@permission_required('cart.add_purchase', raise_exception=True)
def make_a_purchase(request):
    cart = Cart.objects.get(user=request.user)
    cart_items = CartItem.objects.filter(cart=cart)
    profile = Profile.objects.get(user=request.user)
    warning_message = None

    total_price = sum(item.device.price * item.quantity for item in cart_items)
    purchased_devices = [{item.device.name: item.quantity} for item in cart_items]
    json_devices = json.dumps(purchased_devices, ensure_ascii=False)

    if request.method == 'POST':
        purchase_form = PurchaseForm(request.POST)

        if purchase_form.is_valid() and profile.balance >= total_price:
            purchase = purchase_form.save(commit=False)
            purchase.user = request.user
            purchase.amount = total_price
            purchase.purchased_devices = json_devices
            purchase.save()

            Profile.objects.filter(id=profile.id).update(balance=profile.balance - total_price)

            cart_items.delete()

            return redirect('device_showcase')
        else:
            warning_message = "У вас недостаточно средств."
    else:
        purchase_form = PurchaseForm()

    return render(request, 'cart/purchase_page.html', {'profile': profile, 'total_price': total_price,
                                                       'purchase_form': purchase_form, 'cart_items': cart_items,
                                                       'warning_message': warning_message})


def dadata_autocomplete(request):
    query = request.GET.get('query', '')
    dadata = Dadata(token=settings.DADATA_API_KEY, secret=settings.DADATA_SECRET_KEY)

    suggestions = dadata.suggest("address", query)
    # print(suggestions[0])
    return JsonResponse({'suggestions': suggestions})
