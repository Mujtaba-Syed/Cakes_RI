from django.urls import path
from .views import GetAllProductsView, RedirectToWhatsAppView

urlpatterns = [
    path('api/get_all_products/', GetAllProductsView.as_view(), name='get_all_products'),
    path('redirect-to-whatsapp/', RedirectToWhatsAppView.as_view(), name='redirect_to_whatsapp'),
]
