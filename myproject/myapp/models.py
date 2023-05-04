from django.db import models
from django.contrib.auth.models import User

class Farmer(models.Model):
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    dob = models.DateField()
    nationality = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def _str_(self):
        return self.name

class Client(models.Model):
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    address = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def _str_(self):
        return self.name

class Product(models.Model):
    CATEGORY_CHOICES = (
        ('fruits', 'Fruits'),
        ('vegetables', 'Vegetables'),
        ('grains', 'Grains'),
        ('livestock', 'Livestock'),
    )

    name = models.CharField(max_length=255)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='products/')
    quantity_in_stock = models.IntegerField(default=0)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    description = models.TextField()

    def _str_(self):
        return self.name

class Order(models.Model):
    PAYMENT_CHOICES = (
        ('cash', 'Cash'),
        ('credit_card', 'Credit Card'),
        ('debit_card', 'Debit Card'),
    )

    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    date_ordered = models.DateTimeField(auto_now_add=True)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_CHOICES)

    def _str_(self):
        return f"Order {self.pk}"

class OrderDetail(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()

    def _str_(self):
         return f"{self.quantity} x {self.product.name} for {self.order.client.name}"

