from django.shortcuts import render
from .serializers import ReviewSerializer
from .models import Review
from rest_framework import generics, permissions
# Create your views here.

class ReviewListCreateView(generics.ListCreateAPIView):
    permission_classes = [permissions.AllowAny]
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer