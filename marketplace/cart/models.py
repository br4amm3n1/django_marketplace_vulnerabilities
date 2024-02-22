from django.db import models
from django.contrib.auth.models import User
from devices.models import Device


class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    items = models.ManyToManyField(Device, through='CartItem')

    def __str__(self):
        return f"Корзина пользователя: {self.user.username}"


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    device = models.ForeignKey(Device, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.device.name} в корзине пользователя: {self.cart.user.username}"


class Purchase(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    delivery_address = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    purchased_devices = models.CharField(max_length=1000, default=None)

    def __str__(self):
        return f"Покупка сделана {self.user.username} в {self.timestamp}"
