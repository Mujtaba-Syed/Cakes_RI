from django.urls import path
from .views import GetAllProductsView, RedirectToWhatsAppView, ContactWhatsAppView  


urlpatterns = [
    path('api/get_all_products/', GetAllProductsView.as_view(), name='get_all_products'),
    path('redirect-to-whatsapp/', RedirectToWhatsAppView.as_view(), name='redirect_to_whatsapp'),
    path('contact-whatsapp/', ContactWhatsAppView.as_view(), name='contact_whatsapp'),
]
