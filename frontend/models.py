from django.db import models
# from ckeditor.fields import RichTextField  # Import the RichTextField

# Create your models here.
class Flavor(models.Model):
    name=models.CharField(max_length=120)
class Cake(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    type = models.CharField(max_length=50, choices=[('Birthday', 'Birthday'), ('Cupcakes', 'Cupcakes'), ('Custom', 'Custom')])
    image = models.ImageField(upload_to='cakes/')
    flavor=models.ManyToManyField(Flavor)
    active = models.BooleanField(default=True)
    
    
class Services(models.Model):
    name=models.CharField(max_length=100)
    description= models.TextField()
    image=models.ImageField(upload_to='services')
    active=models.BooleanField(default=True)
