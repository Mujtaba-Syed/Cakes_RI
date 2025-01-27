from django.contrib import admin
from .models import Cake, Services, Flavor
# Register your models here.
admin.site.register(Cake)
admin.site.register(Flavor)
admin.site.register(Services)