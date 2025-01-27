from django.db import models
from django.contrib.auth.models import User,AbstractUser,BaseUserManager,Permission,Group
from io import BytesIO
from PIL import Image
from django.core.files import File
from django.conf import settings
from .user import *
from.mixins import *
from django.contrib.auth.models import User
# Create your models here.


class UserProfileManager(BaseUserManager):
    def create_user(self, email, full_name, phone_number, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, full_name=full_name, phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, full_name, phone_number, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, full_name, phone_number, password, **extra_fields)

class UserProfile(AbstractUser):
    USER_TYPE_CHOICES = [
        ('customer', 'Customer'),
        ('seller', 'Seller'),
        ('admin', 'Admin'),
    ]

    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
        ('none', 'Prefer not to say'),
    ]
    user = models.OneToOneField(User,related_name='user_profile', on_delete=models.CASCADE, null=True, blank=True)
    full_name = models.CharField(max_length=200)
    email = models.EmailField(max_length=200, unique=True)
    phone_number = models.IntegerField(null=True, blank=True)
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES)
    gender = models.CharField(max_length=20, choices=GENDER_CHOICES)
    date_of_birth = models.DateTimeField(null=True, blank=True)

    objects = UserProfileManager()

    groups = models.ManyToManyField(
        Group,
        verbose_name=('groups'),
        blank=True,
        related_name='user_profiles_groups',
        help_text=(
            'The groups this user belongs to. A user will get all permissions '
            'granted to each of their groups.'
        ),
    )
    
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name=('user permissions'),
        blank=True,
        related_name='user_profiles_permissions',
        help_text=('Specific permissions for this user.'),
    )
    
    def is_admin(self):
        return self.user_type == UserTypeChoice.admin_user()

    def is_customer(self):
        return self.user_type == UserTypeChoice.customer_user()

    def is_seller(self):
        return self.user_type == UserTypeChoice.seller_user()

    def save(self, *args, **kwargs):
        if not self.username:
            self.username = self.user.username
        super().save(*args, **kwargs)
    def __str__(self):
        return self.full_name or f"User Profile {self.pk}"
    

    


class Product(models.Model):
    CATEGORY_CHOICES = [
        ('Cakes', 'Cakes'),
        ('Cupcakes', 'Cupcakes'),
        ('Bouquets', 'Bouquets'),
        ('Donuts', 'Donuts'),
        ('Brownies', 'Brownies'),
    ]
    name=models.CharField(max_length=200)
    price=models.DecimalField(decimal_places=2, max_digits=9)
    digital=models.BooleanField(default=False, null=True, blank=True)  # buy default every item is physical  
    image=models.ImageField(null=True, blank=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='Cakes')  # Add this line

    
    def __str__(self):
        return self.name
    
        # if admin post a product without image then it generate an error the function will remove this errror

    @property
    def imageURL(self):
        try:
            url=self.image.url
        except:
            url= ''
        return url

    
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