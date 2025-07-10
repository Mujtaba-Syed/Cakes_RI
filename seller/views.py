from django.shortcuts import render
from django.views.generic import TemplateView
from django.http import JsonResponse
import json

class DashboardView(TemplateView):
    template_name = 'seller/dashboard.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        yearly_sales_data = [5000, 6000, 8000, 10000, 12000, 15000, 18000, 20000, 22000, 25000, 28000, 30000]
        monthly_sales_data = [400, 600, 800, 1200, 1500, 1800, 2000, 2200, 2500, 2800, 3000, 3500]
        
        context.update({
            'yearly_sales_data': json.dumps(yearly_sales_data),
            'monthly_sales_data': json.dumps(monthly_sales_data),
        })
        return context
