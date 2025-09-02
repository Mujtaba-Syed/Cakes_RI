from django.contrib import admin
from .models import Cake, Services, Flavor

# Register your models here.
# admin.site.register(Cake)

class FlavorAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

class CakeAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'type', 'active')
    list_filter = ('type', 'active')
    search_fields = ('name', 'description')
    filter_horizontal = ('flavor',)

class ServicesAdmin(admin.ModelAdmin):
    list_display = ('name', 'active')
    list_filter = ('active',)
    search_fields = ('name', 'description')

admin.site.register(Flavor, FlavorAdmin)
admin.site.register(Services, ServicesAdmin)