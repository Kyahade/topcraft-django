from django import forms
from .models import Worker, InventoryItem, Order, Project, CustomRequest, StandardProduct

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
        fields = ['customer_name', 'product_name', 'quantity', 'status']

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = '__all__'
        
class CustomRequestForm(forms.ModelForm):
    class Meta:
        model = CustomRequest
        fields = '__all__'
        
class StandardProductForm(forms.ModelForm):
    class Meta:
        model = StandardProduct
        fields = '__all__'