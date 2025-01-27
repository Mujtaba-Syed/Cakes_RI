from django.shortcuts import render
from django.http import JsonResponse
import json

def dashboard(request):
    yearly_sales_data = [5000, 6000, 8000, 10000, 12000, 15000, 18000, 20000, 22000, 25000, 28000, 30000]
    monthly_sales_data = [400, 600, 800, 1200, 1500, 1800, 2000, 2200, 2500, 2800, 3000, 3500]

    return render(
        request,
        'seller/dashboard.html',
        {
            'yearly_sales_data': json.dumps(yearly_sales_data),
            'monthly_sales_data': json.dumps(monthly_sales_data),
        }
    )
