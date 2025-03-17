from rest_framework import generics
from .models import Review
from .serializers import ReviewSerializer

class ReviewListView(generics.ListAPIView):
    queryset = Review.objects.filter(is_active=True).order_by('-date')[:5]
    serializer_class = ReviewSerializer
