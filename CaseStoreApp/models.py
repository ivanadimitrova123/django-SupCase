from django.db import models
from django.contrib.auth.models import AbstractUser, User


class Product(models.Model):
    name = models.CharField(max_length=100)
    color = models.CharField(max_length=100)
    phone_type = models.CharField(max_length=100)
    material = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField()
    image = models.ImageField(upload_to="case_images/")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cart for {self.user.username}"


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, null=True, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.product} ({self.quantity}) in Cart"


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.SET_NULL, null=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    counrty = models.CharField(max_length=50)
    city_postal = models.CharField(max_length=50)
    shipping_address = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=50)
    pay_with_card = models.BooleanField(default=True)

    def __str__(self):
        return f"Order #{self.pk} by {self.user}"

    def calculate_total_amount(self):
        total = 0
        cart_items = self.cart.items.all()
        for cart_item in cart_items:
            total += cart_item.product.price * cart_item.quantity
        return total
