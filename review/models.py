from django.db import models
from base.models import UserProfile, Product

# Create your models here.
class Review(models.Model):
    user=models.ForeignKey(UserProfile, on_delete=models.CASCADE, null=True, blank=True)
    product=models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True)
    name=models.CharField(max_length=100)
    email=models.EmailField(max_length=100)
    review=models.TextField()
    rating=models.IntegerField()
    date=models.DateTimeField(auto_now_add=True)
    is_active=models.BooleanField(default=True) 
    def __str__(self):
        return self.name