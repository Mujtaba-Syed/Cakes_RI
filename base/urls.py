from django.urls import path
from . import views

urlpatterns = [
    # Class-based views
    path('store/', views.StoreView.as_view(), name='store'),    
    path('cake/', views.CakesView.as_view(), name='cakes'),    
    path('cupcakes/', views.CupcakeView.as_view(), name='cupcakes'),    
    path('bouquet/', views.BouquetView.as_view(), name='bouquets'),    
    path('brownie/', views.BrownieView.as_view(), name='brownies'),    
    path('donut/', views.DonutView.as_view(), name='donuts'),    
    path('cart/', views.CartView.as_view(), name='cart'),    
    path('checkout/', views.CheckoutView.as_view(), name='checkout'),    
    path('update_item/', views.UpdateItemView.as_view(), name='update_item'),    
    path('process_order/', views.ProcessOrderView.as_view(), name='product_order'),   
    path('login/', views.LoginView.as_view(), name='login'),
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
]