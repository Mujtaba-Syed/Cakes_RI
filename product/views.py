from django.shortcuts import redirect
from django.views.generic import View
from rest_framework.views import APIView
from .serializers import GetAllProductSerializers
from base.models import Product
from rest_framework.response import Response
from django.http import HttpRequest
# Create your views here.


class GetAllProductsView(APIView):
    serializer_class= GetAllProductSerializers
    def get(self, request):
        category= request.query_params.get('category', None)
        if category:
            products= Product.objects.filter(category=category, is_active=True)
        else:  
            products = Product.objects.filter(is_active=True)
        serializer = GetAllProductSerializers(products, many=True)
        return Response(serializer.data)
    
    
class RedirectToWhatsAppView(View):
    def get(self, request: HttpRequest):
        base_url = "https://wa.me/3354919379"
        
        cake_name = request.GET.get('cake_name', 'Unknown Cake')
        cake_price = request.GET.get('cake_price', '0')
        cake_desc = request.GET.get('cake_desc', 'No description available')
        cake_type = request.GET.get('cake_type', 'Unknown Type')

        message = (
            f"Hi , I would like to order:\n"
            f"🍰 *{cake_name}*\n"
            f"💰 Price: Rs {cake_price}\n"
            f"📜 Description: {cake_desc}\n"
            f"📦 Type: {cake_type}\n"
            f"Please let me know the next steps!"
        )

        encoded_message = message.replace(" ", "%20").replace("\n", "%0A")

        whatsapp_url = f"{base_url}?text={encoded_message}"

        return redirect(whatsapp_url)