from django.db import models
from django.contrib.auth.models import User

class Worker(models.Model):
    
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    name = models.CharField(max_length=100)
    role = models.CharField(max_length=100)
    skill = models.CharField(max_length=100)

    status = models.CharField(
        max_length=50,
        default="Available"
    )

    def __str__(self):
        return self.name


class InventoryItem(models.Model):
    item_name = models.CharField(max_length=100)
    category = models.CharField(max_length=100)
    quantity = models.IntegerField(default=0)
    unit = models.CharField(max_length=50)

    @property
    def stock_status(self):
        if self.quantity <= 5:
            return "Low Stock"
        elif self.quantity <= 15:
            return "Medium Stock"
        else:
            return "Available"

    def __str__(self):
        return self.item_name

class Project(models.Model):
    order = models.OneToOneField(
    'Order',
    on_delete=models.CASCADE,
    null=True,
    blank=True
    )   

    project_name = models.CharField(max_length=100)

    assigned_worker = models.ForeignKey(
        Worker,
        on_delete=models.SET_NULL,
        null=True
    )

    status = models.CharField(
        max_length=50,
        default="In Production"
    )

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
    
class StandardProduct(models.Model):
    product_name = models.CharField(max_length=100)
    category = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=50, default="Available")

    def __str__(self):
        return self.product_name
    
class Order(models.Model):
    ORDER_TYPE_CHOICES = (
        ('standard', 'Standard Order'),
        ('custom', 'Custom Order'),
    )

    STATUS_CHOICES = (
        ('pending', 'Pending Review'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
        ('assigned', 'Assigned to Worker'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
    )

    customer = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    standard_product = models.ForeignKey(StandardProduct, on_delete=models.SET_NULL, null=True, blank=True)
    order_type = models.CharField(max_length=20, choices=ORDER_TYPE_CHOICES, default='standard')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    assigned_worker = models.ForeignKey(Worker, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        customer_name = self.customer.username if self.customer else "No Customer"
        return f"{customer_name} - {self.order_type} - {self.status}"