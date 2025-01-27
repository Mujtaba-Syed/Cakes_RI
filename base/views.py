from django.shortcuts import render, redirect,get_object_or_404
from django.http import JsonResponse
from .models import *
import uuid
import json
import datetime
from .utils import *
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from .forms import SignUpForm
from django.contrib.auth.decorators import login_required
from django.urls import resolve



# Create your views here.

# home function 
def Home(request):
    user = request.user
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
            # Handle the case when the user profile does not exist
            pass

    context = {'items': items, 'order': order, 'cartItems': cartItems, 'user_profile': user_profile}
    return render(request, 'base/home.html', context)

#cart function
def Cart(request):
    data = cartData(request)
    items = data['items']
    order = data['order']
    cartItems = data['cartItems']

    # Get the current view's URL
    current_url = request.resolver_match.url_name

    # Create a dictionary mapping category names to their respective URLs
    category_urls = {
        'cakes': 'cakes',
        'cupcakes': 'cupcakes',
        # Add other categories...
    }

    # Get the category parameter from the current URL
    category = request.GET.get('category', None)

    # If the category is valid, update the current_url to the category's URL
    if category and category in category_urls:
        current_url = category_urls[category]

    context = {
        'items': items,
        'order': order,
        'cartItems': cartItems,
        'current_url': current_url,
    }

    return render(request, 'base/cart.html', context)
#store function
def Store(request):
    data=cartData(request)
    cartItems=data['cartItems']
    
    
    product=Product.objects.all()
    
    context={'products':product, 'cartItems':cartItems}
    return render(request, 'base/store.html', context)



#cupcake function
def Cupcake(request):
    data=cartData(request)
    cartItems=data['cartItems']
    
    
    cupcakes = Product.objects.filter(category='Cupcakes')
    
    context={'products':cupcakes, 'cartItems':cartItems}
    return render(request, 'base/cupcakes.html', context)

#donut function
def Donut(request):
    data=cartData(request)
    cartItems=data['cartItems']
    
    
    donut = Product.objects.filter(category='Donuts')
    
    context={'products':donut, 'cartItems':cartItems}
    return render(request, 'base/donut.html', context)

#bouquet function
def Bouquet(request):
    data=cartData(request)
    cartItems=data['cartItems']
    
    
    bouquet = Product.objects.filter(category='Bouquets')
    
    context={'products':bouquet, 'cartItems':cartItems}
    return render(request, 'base/bouquet.html', context)


#brownie function
def Brownie(request):
    data=cartData(request)
    cartItems=data['cartItems']
    
    
    brownie = Product.objects.filter(category='Brownies')
    
    context={'products':brownie, 'cartItems':cartItems}
    return render(request, 'base/brownie.html', context)


#donut function
def Donut(request):
    data=cartData(request)
    cartItems=data['cartItems']
    
    
    donut = Product.objects.filter(category='Donuts')
    
    context={'products':donut, 'cartItems':cartItems}
    return render(request, 'base/donut.html', context)

    

#cakes function
def Cakes(request):
    data=cartData(request)
    cartItems=data['cartItems']
    
    
    cakes = Product.objects.filter(category='Cakes')

    context={'products':cakes, 'cartItems':cartItems}
    return render(request, 'base/cakes.html', context)


#checkout function

# def Checkout(request):

#     data=cartData(request)
#     cartItems=data['cartItems']
#     items=data['items']
#     order=data['order']
#     context={'items':items, 'order':order, 'cartItems':cartItems}
#     return render(request, 'base/checkout.html', context)


def Checkout(request):
    data = cartData(request)
    items = data['items']
    order = data['order']
    cartItems = data['cartItems']

    # Get the current view's URL
    current_url = request.resolver_match.url_name

    # Create a dictionary mapping category names to their respective URLs
    category_urls = {
        'cakes': 'cakes',
        'cupcakes': 'cupcakes',
        # Add other categories...
    }

    # Get the category parameter from the current URL
    category = request.GET.get('category', None)

    # If the category is valid, update the current_url to the category's URL
    if category and category in category_urls:
        current_url = category_urls[category]

    context = {
        'items': items,
        'order': order,
        'cartItems': cartItems,
        'current_url': current_url,
    }

    return render(request, 'base/checkout.html', context)

def updateItem(request):
    data= json.loads(request.body)
    productId= data['productId']
    action = data['action']

    customer=request.user.user_profile
    product= Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(user=customer, complete=False)
    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)
    if action == 'add':
        orderItem.quantity = (orderItem.quantity +1)
    elif action == 'remove':    
        orderItem.quantity = (orderItem.quantity -1)
    orderItem.save()
    
        
    if orderItem.quantity<=0:
        orderItem.delete()
        
    order_items=order.orderitem_set.all()
    items=[{
        'product':{
            'id':item.product.id,
            'name':item.product.name,
            'price':item.product.price,
            'imageURL':item.product.imageURL
        },
        'quantity':item.quantity,
        'get_total':item.get_total,
    } 
        for item in order_items]
    cart_info={
            'get_cart_total':order.get_cart_total,
            'get_cart_items':order.get_cart_items,
            'shipping':order.shipping,
        }
    response_data={'items':items, 'order':cart_info}
    return JsonResponse(response_data, safe=False)

@csrf_exempt
def processOrder(request):
    # transaction_id = str(uuid.uuid4())
    transaction_id=datetime.datetime.now().timestamp()
    data= json.loads(request.body)
    
    if request.user.is_authenticated:
        customer=request.user.user_profile
        # print("customerrrrrrrrrrr", customer)
        order,created=Order.objects.get_or_create(user=customer, complete=False)


    else:
        customer, order=guestOrder(request, data)
        
    total=float(data['form']['total'])
    order.transaction_id = transaction_id
    
    if total == order.get_cart_total:
        order.complete=True
    order.save()
    
    if order.shipping== True:
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



def Login_view(request):
    if request.method=='POST':
        username=request.POST.get('username')
        password=request.POST.get('password')
        user=authenticate(request,username=username, password=password)
        
        if user is not  None:
            login(request, user)
            if user.user_profile.user_type==UserTypeChoice.seller_user():
                return redirect('seller:dashboard')
            else:
                return redirect('home')
        
    return render(request,'base/login.html')

def SignUp_view(request):
    context = {}

    if request.method == 'POST':
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
        else:
            context = {'form': form}
    else:
        form = SignUpForm()
        context = {'form': form}

    return render(request, 'base/signup.html', context)

def logout_view(request):
    logout(request)
    return redirect('home')



