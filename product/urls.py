from django.urls import path
from .views import GetAllProductsView, redirect_to_whatsapp

urlpatterns = [
    path('api/get_all_products/', GetAllProductsView.as_view(), name='get_all_products'),
    path('redirect-to-whatsapp/', redirect_to_whatsapp, name='redirect_to_whatsapp'),

]
