from django.urls import path
from .views import ReviewListView

urlpatterns = [
    path('api/reviews/', ReviewListView.as_view(), name='review-list-create'),
]
