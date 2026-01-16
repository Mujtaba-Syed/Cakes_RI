from django.urls import path
from . import views

urlpatterns = [
    # Class-based views
    path('', views.HomeView.as_view(), name='home'),
    path('aboutus/', views.AboutUsView.as_view(), name='aboutus'),
    path('menu/', views.MenuView.as_view(), name='menu'),
    path('team/', views.TeamView.as_view(), name='team'),
    path('services/', views.ServiceView.as_view(), name='services'),
    path('testimonial/', views.TestimonialView.as_view(), name='testimonial'),
    path('contactus/', views.ContactUsView.as_view(), name='contactus'),
    path('registration/', views.RegistrationView.as_view(), name='register'),
    path('cart/', views.AddToCartView.as_view(), name='cart'),
    path('checkout/', views.CheckoutView.as_view(), name='checkout'),
    # SEO
    path('robots.txt', views.robots_txt, name='robots_txt'),
    # Google Search Console verification
    path('google76a61c0a0e658004.html', lambda request: views.google_verification(request, 'google76a61c0a0e658004.html'), name='google_verification'),
]