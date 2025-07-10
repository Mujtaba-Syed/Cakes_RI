from django.shortcuts import render
from .models import Cake, Services, Flavor
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import View, TemplateView, ListView
from django.contrib import messages
from django.core.serializers.json import DjangoJSONEncoder

# Create your views here.

class HomeView(TemplateView):
    template_name = 'frontend/home.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        birthday_cakes = Cake.objects.filter(type='Birthday', active=True)
        cup_cakes = Cake.objects.filter(type='Cupcakes', active=True)
        custom_cakes = Cake.objects.filter(type='Custom', active=True)
        context.update({
            'birthday_cakes': birthday_cakes,
            'cup_cakes': cup_cakes,
            'custom_cakes': custom_cakes,
        })
        return context


class AboutUsView(TemplateView):
    template_name = 'frontend/about.html'


class MenuView(TemplateView):
    template_name = 'frontend/menu.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        birthday_cakes = Cake.objects.filter(type='Birthday', active=True)
        cup_cakes = Cake.objects.filter(type='Cupcakes', active=True)
        custom_cakes = Cake.objects.filter(type='Custom', active=True)
        context.update({
            'birthday_cakes': birthday_cakes,
            'cup_cakes': cup_cakes,
            'custom_cakes': custom_cakes,
            'include_mode': False 
        })
        return context


class TeamView(TemplateView):
    template_name = 'frontend/team.html'


class ServiceView(ListView):
    model = Services
    template_name = 'frontend/services.html'
    context_object_name = 'services'
    
    def get_queryset(self):
        return Services.objects.filter(active=True)


class TestimonialView(TemplateView):
    template_name = 'frontend/testimonial.html'


class ContactUsView(TemplateView):
    template_name = 'frontend/contact.html'


class RegistrationView(TemplateView):
    template_name = 'frontend/sign.html'


class AddToCartView(View):
    def get(self, request, *args, **kwargs):
        cake_name = request.GET.get('cake_name')
        cake_price = request.GET.get('cake_price')
        cake_desc =request.GET.get('cake_desc')
        cake_type=request.GET.get('cake_type')
        
        if cake_type in ['Cupcakes', 'Custom']:
            flavor=Flavor.objects.all()
        else:
            flavor=None

        context = {
            'cake_name': cake_name,
            'cake_price': cake_price,
            'cake_desc': cake_desc,
            'cake_type':cake_type,
            'flavor': flavor,
        }
        print(context)  

        return render(request, 'frontend/cart.html', context)

    def post(self, request, *args, **kwargs):
        cake_id = self.request.POST.get('cake_id')
        # cake_size = self.request.POST.get('cake_size')
        cake_name = request.POST.get('cake_name')
        cake_price = request.POST.get('cake_price')
        cake_desc =request.POST.get('cake_desc')
        # cake_flavor=request.POST.get('flavor')
        cake_type = request.POST.get('cake_type')

        cake = get_object_or_404(Cake, pk=cake_id)


        print('.......fff',cake_name, cake_price)
        # total_amount = cake.price * int(cake_size)

        # Convert Decimal to string
        cake_price_str = str(cake_price)
        # total_amount_str = str(total_amount)

        cart = request.session.get('cart', {})
        cart[cake_id] = {
            'name': cake_name,
            'cake_price': cake_price_str,
            # 'size': cake_size,
            # 'price': total_amount_str,
            'cake_desc': cake_desc,
            'type':cake_type,
        }
        request.session['cart'] = cart

        messages.success(request, f"{cake.name} added to cart successfully.")
        return redirect('cart')
    
    
class CheckoutView(View):
    def get(self, request, *args, **kwargs):
        cake_name = request.GET.get('cake_name')
        cake_price = float(request.GET.get('cake_price'))
        selected_size = int(request.GET.get('cake_size'))
        # selected_size = 3
        
        print("Cake Price:", cake_price)  # Add this line for debugging
        print("Cake Size.......:",selected_size)  # Add this line for debugging


        # Calculate total amount based on selected size and cake price
        total_amount = cake_price * selected_size

        context = {
            'cake_name': cake_name,
            'cake_price': cake_price,
            'selected_size': selected_size,
            'total_amount': total_amount,
        }
        return render(request, 'frontend/checkout.html', context)
