from django.db import models
from category.models import Category
from django.urls import reverse

#product table

class Product(models.Model):
    product_name = models.CharField(max_length=100,unique=True)
    slug         = models.SlugField(max_length=200,unique=True)
    description  = models.TextField(max_length=500,blank=True)
    price        = models.IntegerField()
    brand        = models.CharField(max_length=100)
    images1      = models.ImageField(upload_to='productimages/')
    images2      = models.ImageField(upload_to='productimages/',blank=True)
    images3      = models.ImageField(upload_to='productimages/',blank=True)
    images4      = models.ImageField(upload_to='productimages/',blank=True)
    stock        = models.IntegerField()
    is_available = models.BooleanField(default=True)
    category     = models.ForeignKey(Category,on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date= models.DateTimeField(auto_now=True)
    
    def get_url(self):
        return reverse('product_detail',args=[self.category.slug,self.slug])
    
    
    
    def __str__(self):
        return self.product_name
# Create your models here.
