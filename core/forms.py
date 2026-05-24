from django import forms
from .models import Worker, InventoryItem, Order, Project, CustomRequest, StandardProduct
from django.utils import timezone

class WorkerForm(forms.ModelForm):
    class Meta:
        model = Worker
        fields = '__all__'

class InventoryItemForm(forms.ModelForm):
    class Meta:
        model = InventoryItem
        fields = '__all__'

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = [
            'customer',
            'standard_product',
            'order_type',
            'status',
            'assigned_worker'
        ]

        widgets = {
            'status': forms.Select(attrs={'class': 'form-select'}),
            'assigned_worker': forms.Select(attrs={'class': 'form-select'}),
        }
class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['project_name', 'status', 'deadline']
        
class AssignWorkerForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['assigned_worker']
        
class CustomRequestForm(forms.ModelForm):
    class Meta:
        model = CustomRequest
        fields = '__all__'
        
class StandardProductForm(forms.ModelForm):
    class Meta:
        model = StandardProduct
        fields = '__all__'