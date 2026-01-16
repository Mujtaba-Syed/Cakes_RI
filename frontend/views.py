from django.shortcuts import render
from .models import Cake, Services, Flavor
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import View, TemplateView, ListView
from django.contrib import messages
from django.core.serializers.json import DjangoJSONEncoder
from django.http import HttpResponse
from django.conf import settings
import os

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


def robots_txt(request):
    """Serve robots.txt file"""
    # Try multiple locations
    possible_paths = []
    
    # Check STATIC_ROOT first (production)
    if hasattr(settings, 'STATIC_ROOT') and settings.STATIC_ROOT:
        possible_paths.append(os.path.join(settings.STATIC_ROOT, 'robots.txt'))
    
    # Check STATICFILES_DIRS
    if hasattr(settings, 'STATICFILES_DIRS') and settings.STATICFILES_DIRS:
        for static_dir in settings.STATICFILES_DIRS:
            possible_paths.append(os.path.join(static_dir, 'robots.txt'))
    
    # Try to read from any available location
    for robots_file_path in possible_paths:
        try:
            if os.path.exists(robots_file_path):
                with open(robots_file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                response = HttpResponse(content, content_type='text/plain')
                response['Cache-Control'] = 'public, max-age=86400'  # Cache for 1 day
                return response
        except (FileNotFoundError, IOError):
            continue
    
    # Fallback robots.txt content if file not found
    content = """User-agent: *
Allow: /

# Sitemap location
Sitemap: https://www.cakebyrimi.com/sitemap.xml

# Disallow admin and private areas
Disallow: /admin/
Disallow: /cart/
Disallow: /checkout/
Disallow: /registration/

# Allow important pages
Allow: /
Allow: /aboutus/
Allow: /menu/
Allow: /services/
Allow: /testimonial/
Allow: /contactus/
Allow: /team/
"""
    response = HttpResponse(content, content_type='text/plain')
    response['Cache-Control'] = 'public, max-age=86400'
    return response


def google_verification(request, filename):
    """
    Serve Google Search Console verification files.
    Files should be placed in static/ directory with name like: google76a61c0a0e658004.html
    """
    # Try multiple locations
    possible_paths = []
    
    # Check STATIC_ROOT first (production)
    if hasattr(settings, 'STATIC_ROOT') and settings.STATIC_ROOT:
        possible_paths.append(os.path.join(settings.STATIC_ROOT, filename))
    
    # Check STATICFILES_DIRS
    if hasattr(settings, 'STATICFILES_DIRS') and settings.STATICFILES_DIRS:
        for static_dir in settings.STATICFILES_DIRS:
            possible_paths.append(os.path.join(static_dir, filename))
    
    # Try to read from any available location
    for file_path in possible_paths:
        try:
            if os.path.exists(file_path):
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                response = HttpResponse(content, content_type='text/html')
                response['Cache-Control'] = 'public, max-age=86400'
                return response
        except (FileNotFoundError, IOError):
            continue
    
    # Return 404 if file not found
    return HttpResponse('File not found', status=404, content_type='text/plain')


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
