from django.contrib import admin
from .models import *
# Register your models here.

class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'category', 'is_active','updated_at','created_at')
    list_filter = ('category', 'is_active')
admin.site.register(UserProfile)
# admin.site.register(Customer)

admin.site.register(Product, ProductAdmin)
