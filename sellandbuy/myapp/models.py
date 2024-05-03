from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Seller(models.Model) :
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.first_name

class Buyer(models.Model) :
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.first_name
    

class Address(models.Model) :
    address = models.CharField(max_length=300)
    user = models.ForeignKey('myapp.Buyer', on_delete=models.CASCADE)

    def __str__(self):
        return self.address
    


class Product(models.Model) :
    code = models.CharField(max_length=7, unique=True, blank=True, null=True) # thala for a reason
    name = models.CharField(max_length=100)
    desc = models.CharField(max_length = 500, blank=True, null=True)
    price = models.IntegerField()
    seller = models.ForeignKey('myapp.Seller', on_delete=models.CASCADE, blank=True, null=True)
    image_field = models.ImageField(default='')

    def __str__(self):
        return f"{self.name} ({self.code})"

from django.core.validators import MinValueValidator, MaxValueValidator

class Reviews(models.Model) :
    product = models.ForeignKey("myapp.Product", on_delete=models.CASCADE)
    provider = models.ForeignKey("myapp.Buyer", on_delete=models.CASCADE)
    stars = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(5)]
    )
    review = models.CharField(max_length=100)

    def __str__(self):
        return self.review
    

class Cart(models.Model) :
    product = models.ForeignKey("myapp.Product", on_delete=models.CASCADE)
    buyer = models.ForeignKey("myapp.Buyer", on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)

    def __str__(self):
        return self.product.name

class Orders(models.Model) :
    product = models.ForeignKey("myapp.Product", on_delete=models.CASCADE)
    buyer = models.ForeignKey("myapp.Buyer", on_delete=models.CASCADE)

    statuses = [
        ('Delivered', 'Delivered'),
        ('On the way', 'On the way'),
        ('Cancelled', 'Cancelled'),
    ]
    status = models.CharField(max_length=20, choices=statuses)
    dateandtime = models.CharField(max_length = 100) # format 30-04-2024-tuesday
    payment_methods = [
        ('Cash on delivery', 'Cash on delivery'),
        ('Credit card', 'Credit card'),
        ('Net banking', 'Net banking'),
    ]
    payment_method = models.CharField(max_length=20, choices=payment_methods)

    def __str__(self):
        return f"{self.product.name} placed by {self.buyer.first_name}"

