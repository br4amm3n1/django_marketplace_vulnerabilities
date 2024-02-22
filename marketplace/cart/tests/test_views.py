from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from cart.models import Cart, CartItem, Purchase
from devices.models import Device
from accounts.models import Profile
from decimal import Decimal


class TestCartViews(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.profile = Profile.objects.create(user=self.user)
        self.device = Device.objects.create(name='Test Device', price=10.0)
        self.cart = Cart.objects.create(user=self.user)
        self.cart_item = CartItem.objects.create(cart=self.cart, device=self.device, quantity=2)

    def test_cart_view(self):
        self.client.force_login(self.user)

        response = self.client.get(reverse('cart'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cart/cart.html')
        self.assertEqual(response.context['cart_items'][0].device, self.device)

    def test_add_to_cart(self):
        self.client.force_login(self.user)

        initial_quantity = self.cart_item.quantity

        response = self.client.get(reverse('add_to_cart', args=[self.device.pk]))
        self.assertEqual(response.status_code, 302)

        cart_item = CartItem.objects.get(cart=self.cart, device=self.device)

        self.assertEqual(cart_item.quantity, initial_quantity + 1)

    def test_remove_from_cart(self):
        self.client.force_login(self.user)

        response = self.client.get(reverse('remove_from_cart', args=[self.cart_item.pk]))
        self.assertEqual(response.status_code, 302)

        with self.assertRaises(CartItem.DoesNotExist):
            CartItem.objects.get(pk=self.cart_item.pk)

    def test_dadata_autocomplete(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('dadata_autocomplete'), {'query': 'some_address'})
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn('suggestions', data)


class TestPurchaseViews(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.profile = Profile.objects.create(user=self.user)
        self.profile.balance = 100.00
        self.profile.save()
        self.device = Device.objects.create(name='Test Device', price=10.0)
        self.cart = Cart.objects.create(user=self.user)
        self.cart_item = CartItem.objects.create(cart=self.cart, device=self.device, quantity=2)
        self.purchase_url = reverse('make_purchase')

    def test_make_a_purchase(self):
        self.client.force_login(self.user)
        response = self.client.post(self.purchase_url, {'delivery_address': 'Test Address'})
        # print(response.content)
        self.assertEqual(response.status_code, 302)  # Check if the view redirects
        self.assertEqual(Purchase.objects.count(), 1)  # Check if a purchase object is created
        self.assertEqual(CartItem.objects.count(), 0)

    def test_insufficient_funds(self):
        self.client.force_login(self.user)

        form_data = {'delivery_address': 'Test Address'}

        self.profile.balance = Decimal('5.0')
        self.profile.save()

        response = self.client.post(reverse('make_purchase'), form_data)

        self.assertEqual(response.status_code, 200)

        self.assertContains(response, "У вас недостаточно средств.")
