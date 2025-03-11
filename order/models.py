from django.db import models
from base.models import UserProfile, Product
# Create your models here.

class Order(models.Model):
    user=models.ForeignKey(UserProfile, on_delete=models.CASCADE, null=True, blank=True)
    date_order=models.DateTimeField(auto_now_add=True)
    complete=models.BooleanField(default=False)
    transaction_ID=models.CharField(max_length=100, null=True)
    
    def __str__(self):
        return str(self.id)
    
    @property
    def shipping(self):
        shipping= False
        orderitems = self.orderitem_set.all()
        for i in orderitems:
            if i.product.digital== False:
                shipping= True
        return shipping
    @property
    def get_cart_total(self):
        orderitems=self.orderitem_set.all()
        total=sum([item.get_total for item in orderitems])
        return total
    
    @property
    def get_cart_items(self):
        orderitems=self.orderitem_set.all()
        total_items=sum([item.quantity for item in orderitems])
        return total_items
    
    
class OrderItem(models.Model):
    product=models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    order= models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    quantity=models.IntegerField(default=0, null=True, blank= True)
    date_added=models.DateTimeField(auto_now_add=True)
    
    @property
    def get_total(self):
        total=self.product.price * self.quantity
        return total
    
class Shipping_Address(models.Model):
    user=models.ForeignKey(UserProfile, on_delete=models.CASCADE, null=True)
    order=models.ForeignKey(Order, on_delete=models.CASCADE,  null=True, blank=False)
    address=models.CharField(max_length=200, null=False)
    city=models.CharField(max_length=200, null=False)
    state=models.CharField(max_length=200, null=False)
    zipcode=models.CharField(max_length=200, null=False)
    country=models.CharField(max_length=200, null=False, default=True)
    date_added=models.DateTimeField(auto_now_add=True)
    contact=models.IntegerField(null=False)
    
    def __str__(self):
        return self.address