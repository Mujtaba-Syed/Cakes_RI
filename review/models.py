from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.
class Review(models.Model):
    name=models.CharField(max_length=100, null=True, blank=True)
    email=models.EmailField(max_length=100, blank=True, null=True)
    review=models.TextField()
    image=models.ImageField(upload_to='review', null=True, blank=True)
    rating=models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    date=models.DateTimeField(auto_now_add=True)
    is_active=models.BooleanField(default=True) 
    def __str__(self):
        return self.name