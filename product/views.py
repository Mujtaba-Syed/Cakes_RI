from django.shortcuts import redirect
from django.views.generic import View
from rest_framework.views import APIView
from .serializers import GetAllProductSerializers
from base.models import Product
from rest_framework.response import Response
from django.http import HttpRequest
from django.db.models import Q
# Create your views here.


class GetAllProductsView(APIView):
    serializer_class= GetAllProductSerializers
    def get(self, request):
        category= request.query_params.get('category', None)
        if category:
            products= Product.objects.filter(category=category, is_active=True).order_by('-updated_at')
        else:  
            products = Product.objects.filter(is_active=True).order_by('-updated_at')
        serializer = GetAllProductSerializers(products, many=True)
        return Response(serializer.data)


class SearchProductsView(APIView):
    serializer_class = GetAllProductSerializers
    
    def get(self, request):
        query = request.query_params.get('q', '').strip()
        category = request.query_params.get('category', None)
        
        if not query:
            return Response({'success': False, 'message': 'Search query is required'}, status=400)
        
        # Search in both name and description fields
        search_filter = Q(name__icontains=query) | Q(description__icontains=query)
        
        # Add category filter if specified
        if category:
            search_filter &= Q(category=category)
        
        products = Product.objects.filter(
            search_filter,
            is_active=True
        ).order_by('-updated_at')
        
        serializer = GetAllProductSerializers(products, many=True)
        
        return Response({
            'success': True,
            'data': serializer.data,
            'query': query,
            'count': products.count()
        })
    
    
class RedirectToWhatsAppView(View):
    def get(self, request: HttpRequest):
        base_url = "https://wa.me/3094817724"
        
        general_message = request.GET.get('message', None)
        
        if general_message:
            message = general_message
        else:
            cake_name = request.GET.get('cake_name', 'Unknown Cake')
            cake_price = request.GET.get('cake_price', '0')
            cake_type = request.GET.get('cake_type', 'Unknown Type')

            message = (
                f"Hi , I would like to order:\n"
                f"*{cake_name}*\n"
                f"Price: Rs {cake_price}\n"
                f"Type: {cake_type}\n"
                f"Please let me know the next steps!"
            )

        encoded_message = message.replace(" ", "%20").replace("\n", "%0A")

        whatsapp_url = f"{base_url}?text={encoded_message}"

        return redirect(whatsapp_url)

class ContactWhatsAppView(View):
    def get(self, request: HttpRequest):
        base_url = "https://wa.me/3094817724"
        
        message = request.GET.get('message', None)
        
        encoded_message = message.replace(" ", "%20").replace("\n", "%0A")
        
        whatsapp_url = f"{base_url}?text={encoded_message}"
        
        return redirect(whatsapp_url)