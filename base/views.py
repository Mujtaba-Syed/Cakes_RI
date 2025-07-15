from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.generic import TemplateView, ListView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.urls import resolve
from .models import *
from .forms import SignUpForm
from order.models import Order, OrderItem, Shipping_Address 
import uuid
import json
import datetime
from .utils import *
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator


# Class-based views

class HomeView(TemplateView):
    template_name = 'base/home.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        user_profile = None
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0}
        cartItems = order['get_cart_items']

        if user.is_authenticated:
            try:
                user_profile = user.user_profile
                order, created = Order.objects.get_or_create(user=user_profile, complete=False)
                items = order.orderitem_set.all()
                cartItems = order.get_cart_items
            except UserProfile.DoesNotExist:
                pass

        context.update({
            'items': items, 
            'order': order, 
            'cartItems': cartItems, 
            'user_profile': user_profile
        })
        return context


class CartView(TemplateView):
    template_name = 'base/cart.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        data = cartData(self.request)
        items = data['items']
        order = data['order']
        cartItems = data['cartItems']

        # Get the current view's URL
        current_url = self.request.resolver_match.url_name

        # Create a dictionary mapping category names to their respective URLs
        category_urls = {
            'cakes': 'cakes',
            'cupcakes': 'cupcakes',
        }

        # Get the category parameter from the current URL
        category = self.request.GET.get('category', None)

        # If the category is valid, update the current_url to the category's URL
        if category and category in category_urls:
            current_url = category_urls[category]

        context.update({
            'items': items,
            'order': order,
            'cartItems': cartItems,
            'current_url': current_url,
        })
        return context


class StoreView(ListView):
    model = Product
    template_name = 'base/store.html'
    context_object_name = 'products'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        data = cartData(self.request)
        context['cartItems'] = data['cartItems']
        return context


class CupcakeView(ListView):
    model = Product
    template_name = 'base/cupcakes.html'
    context_object_name = 'products'
    
    def get_queryset(self):
        return Product.objects.filter(category='Cupcakes')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        data = cartData(self.request)
        context['cartItems'] = data['cartItems']
        return context


class DonutView(ListView):
    model = Product
    template_name = 'base/donut.html'
    context_object_name = 'products'
    
    def get_queryset(self):
        return Product.objects.filter(category='Donuts')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        data = cartData(self.request)
        context['cartItems'] = data['cartItems']
        return context


class BouquetView(ListView):
    model = Product
    template_name = 'base/bouquet.html'
    context_object_name = 'products'
    
    def get_queryset(self):
        return Product.objects.filter(category='Bouquets')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        data = cartData(self.request)
        context['cartItems'] = data['cartItems']
        return context


class BrownieView(ListView):
    model = Product
    template_name = 'base/brownie.html'
    context_object_name = 'products'
    
    def get_queryset(self):
        return Product.objects.filter(category='Brownies')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        data = cartData(self.request)
        context['cartItems'] = data['cartItems']
        return context


class CakesView(ListView):
    model = Product
    template_name = 'base/cakes.html'
    context_object_name = 'products'
    
    def get_queryset(self):
        return Product.objects.filter(category='Cakes')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        data = cartData(self.request)
        context['cartItems'] = data['cartItems']
        return context


class CheckoutView(TemplateView):
    template_name = 'base/checkout.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        data = cartData(self.request)
        items = data['items']
        order = data['order']
        cartItems = data['cartItems']

        # Get the current view's URL
        current_url = self.request.resolver_match.url_name

        # Create a dictionary mapping category names to their respective URLs
        category_urls = {
            'cakes': 'cakes',
            'cupcakes': 'cupcakes',
        }

        # Get the category parameter from the current URL
        category = self.request.GET.get('category', None)

        # If the category is valid, update the current_url to the category's URL
        if category and category in category_urls:
            current_url = category_urls[category]

        context.update({
            'items': items,
            'order': order,
            'cartItems': cartItems,
            'current_url': current_url,
        })
        return context


class UpdateItemView(View):
    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        productId = data['productId']
        action = data['action']

        customer = request.user.user_profile
        product = Product.objects.get(id=productId)
        order, created = Order.objects.get_or_create(user=customer, complete=False)
        orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)
        
        if action == 'add':
            orderItem.quantity = (orderItem.quantity + 1)
        elif action == 'remove':    
            orderItem.quantity = (orderItem.quantity - 1)
        orderItem.save()
        
        if orderItem.quantity <= 0:
            orderItem.delete()
            
        order_items = order.orderitem_set.all()
        items = [{
            'product': {
                'id': item.product.id,
                'name': item.product.name,
                'price': item.product.price,
                'imageURL': item.product.imageURL
            },
            'quantity': item.quantity,
            'get_total': item.get_total,
        } for item in order_items]
        
        cart_info = {
            'get_cart_total': order.get_cart_total,
            'get_cart_items': order.get_cart_items,
            'shipping': order.shipping,
        }
        response_data = {'items': items, 'order': cart_info}
        return JsonResponse(response_data, safe=False)


@method_decorator(csrf_exempt, name='dispatch')
class ProcessOrderView(View):
    def post(self, request, *args, **kwargs):
        transaction_id = datetime.datetime.now().timestamp()
        data = json.loads(request.body)
        
        if request.user.is_authenticated:
            customer = request.user.user_profile
            order, created = Order.objects.get_or_create(user=customer, complete=False)
        else:
            customer, order = guestOrder(request, data)
            
        total = float(data['form']['total'])
        order.transaction_id = transaction_id
        
        if total == order.get_cart_total:
            order.complete = True
        order.save()
        
        if order.shipping == True:
            Shipping_Address.objects.create(
                user=request.user.user_profile,
                order=order,
                address=data['shipping']['address'],
                city=data['shipping']['city'],
                state=data['shipping']['state'],
                zipcode=data['shipping']['zipcode'],
                country=data['shipping']['country'],
                contact=data['shipping']['contact'],
            )
        return JsonResponse('Payment Done', safe=False)


class LoginView(TemplateView):
    template_name = 'base/login.html'
    
    def post(self, request, *args, **kwargs):
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            if user.user_profile.user_type == UserTypeChoice.seller_user():
                return redirect('seller:dashboard')
            else:
                return redirect('home')
        
        return self.get(request, *args, **kwargs)


class SignUpView(TemplateView):
    template_name = 'base/signup.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if 'form' not in context:
            context['form'] = SignUpForm()
        return context
    
    def post(self, request, *args, **kwargs):
        form = SignUpForm(request.POST)
        if form.is_valid():
            # Create a new user
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password1'],
                email=form.cleaned_data['email']
            )

            # Create a corresponding UserProfile
            user_profile = UserProfile(
                user=user,
                full_name=form.cleaned_data['fullname'],
                email=form.cleaned_data['email'],
                phone_number=form.cleaned_data['phone_number'],
                user_type=form.cleaned_data['user_type'],
                gender=form.cleaned_data['gender'],
                date_of_birth=form.cleaned_data['date_of_birth']
            )
            user_profile.save()

            # Authenticate and login the user
            user = authenticate(request, username=user.username, password=form.cleaned_data['password1'])
            login(request, user)

            return redirect('home')
        
        return self.render_to_response({'form': form})


class LogoutView(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect('home')



