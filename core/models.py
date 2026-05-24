from django.db import models
from django.contrib.auth.models import User

class Worker(models.Model):
    name = models.CharField(max_length=100)
    role = models.CharField(max_length=100)
    skill = models.CharField(max_length=100)
    status = models.CharField(max_length=50, default="Available")

    def __str__(self):
        return self.name


class InventoryItem(models.Model):
    item_name = models.CharField(max_length=100)
    category = models.CharField(max_length=100)
    quantity = models.IntegerField()
    unit = models.CharField(max_length=50)
    status = models.CharField(max_length=50, default="Available")

    def __str__(self):
        return self.item_name


class Order(models.Model):
    customer_name = models.CharField(max_length=100)
    product_name = models.CharField(max_length=100)
    quantity = models.IntegerField()
    status = models.CharField(max_length=50, default="Pending")
    order_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.customer_name


class Project(models.Model):
    project_name = models.CharField(max_length=100)
    assigned_worker = models.ForeignKey(Worker, on_delete=models.SET_NULL, null=True)
    status = models.CharField(max_length=50, default="In Production")
    deadline = models.DateField()

    def __str__(self):
        return self.project_name
    
class UserProfile(models.Model):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('worker', 'Worker'),
        ('customer', 'Customer'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)

    def __str__(self):
        return f"{self.user.username} - {self.role}"
    
class CustomRequest(models.Model):
    customer_name = models.CharField(max_length=100)
    furniture_type = models.CharField(max_length=100)
    description = models.TextField()
    budget = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=50, default="Pending Review")
    request_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.furniture_type
    
class CustomRequest(models.Model):
    customer_name = models.CharField(max_length=100)
    furniture_type = models.CharField(max_length=100)
    description = models.TextField()
    budget = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=50, default="Pending Review")
    request_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.furniture_type
    
class StandardProduct(models.Model):
    product_name = models.CharField(max_length=100)
    category = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=50, default="Available")

    def __str__(self):
        return self.product_name