from django.contrib import admin
from .models import Worker, InventoryItem, Order, Project, UserProfile, CustomRequest, StandardProduct

admin.site.register(UserProfile)
admin.site.register(Worker)
admin.site.register(InventoryItem)
admin.site.register(Order)
admin.site.register(Project)
admin.site.register(CustomRequest)
admin.site.register(StandardProduct)