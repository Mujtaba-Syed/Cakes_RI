from django.contrib import admin
from .models import *
# Register your models here.

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'category', 'is_active')
    list_filter = ('category', 'is_active')
admin.site.register(UserProfile)
# admin.site.register(Customer)

admin.site.register(Product, ProductAdmin)
