from email.mime import image

from django import forms
from .models import Worker, InventoryItem, Order, Project, CustomRequest, StandardProduct, UserProfile
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
        
class CustomerProfileForm(forms.ModelForm):
    username = forms.CharField(max_length=150)
    email = forms.EmailField(required=True)

    new_password = forms.CharField(
        widget=forms.PasswordInput(),
        required=False
    )

    confirm_password = forms.CharField(
        widget=forms.PasswordInput(),
        required=False
    )

    class Meta:
        model = UserProfile
        fields = ['profile_image']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        if self.user:
            self.fields['username'].initial = self.user.username
            self.fields['email'].initial = self.user.email

        for field in self.fields.values():
            field.widget.attrs.update({
                'class': 'form-control'
            })

    def clean(self):
        cleaned_data = super().clean()

        new_password = cleaned_data.get('new_password')
        confirm_password = cleaned_data.get('confirm_password')

        if new_password:
            if new_password != confirm_password:
                raise forms.ValidationError("Passwords do not match.")

            if len(new_password) < 8:
                raise forms.ValidationError("Password must be at least 8 characters long.")
            

        return cleaned_data
    
    def clean_profile_image(self):
        image = self.cleaned_data.get('profile_image')

        if image:
            valid_types = ['image/jpeg', 'image/png', 'image/webp']

            if image.content_type not in valid_types:
                raise forms.ValidationError(
                    "Only JPG, PNG, and WEBP images are allowed."
                )

        return image
    
    def save(self, commit=True):
        profile = super().save(commit=False)

        if self.user:
            self.user.username = self.cleaned_data['username']
            self.user.email = self.cleaned_data['email']

            new_password = self.cleaned_data.get('new_password')

            if new_password:
                self.user.set_password(new_password)

            if commit:
                self.user.save()
                profile.save()

        return profile