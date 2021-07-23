from accounts.models import Account
from django.db import models
from category.models import Category
from django.urls import reverse
from datetime import date
from django.db.models import Avg, Count
from .utils import generate_ref_code


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
    offer_price  =models.FloatField(null=True)
    offer_percentage  =models.FloatField(null=True)
    
    def get_url(self):
        return reverse('product_detail',args=[self.category.slug,self.slug])
    def check_status(self):
        today = date.today()
        today1 = today.strftime("%Y-%m-%d")
        if ProductOffer.objects.filter(product=self.id).exists():
            prod=ProductOffer.objects.get(product=self.id)
            if str(prod.offer_end)< today1:
                return False
            else:
                return True
     
        if CategoryOffer.objects.filter(category=self.category.id).exists():
            cat=CategoryOffer.objects.get(category=self.category.id)
            if str(cat.offer_end)< today1:
                print("false")
                return False
            else:
                print("true")
                return True
        else:
            return False
    def __str__(self):
        return self.product_name
        
    def averageReview(self):
        reviews = ReviewRating.objects.filter(product=self, status=True).aggregate(average=Avg('rating'))
        avg = 0
        if reviews['average'] is not None:
            avg = float(reviews['average'])
        return avg

    def countReview(self):
        reviews = ReviewRating.objects.filter(product=self, status=True).aggregate(count=Count('id'))
        count = 0
        if reviews['count'] is not None:
            count = int(reviews['count'])
        return count
    
    
# Create your models here.

class CategoryOffer(models.Model):
    category = models.OneToOneField(Category,on_delete=models.CASCADE)
    offer=models.IntegerField()
    offer_start=models.DateField()
    offer_end=models.DateField()
    
    def check_expired(self):
        today = date.today()
        today1 = today.strftime("%Y-%m-%d")
        if str(self.offer_end)< today1:
            return False
        else:
            return True
class ProductOffer(models.Model):
    product=models.OneToOneField(Product,on_delete=models.CASCADE)
    offer=models.IntegerField()
    offer_start=models.DateField()
    offer_end=models.DateField()
    
    def check_expired(self):
        today=date.today()
        today1=today.strftime("%Y-%m-%d")
        if str(self.offer_end)< today1:
            return False
        else:
            return True

class coupon(models.Model):
    coupon_code=models.CharField(max_length=20)
    coupon_rate=models.FloatField()
    coupon_start=models.DateField()
    coupon_end=models.DateField()
    
    def check_expired(self):
        today=date.today()
        today1=today.strftime("%Y-%m-%d")
        if str(self.coupon_end)< today1:
            return False
        else:
            return True

class UsedOffer(models.Model):
    user=models.ForeignKey(Account,on_delete=models.CASCADE)
    coupon=models.ForeignKey(coupon,on_delete=models.CASCADE)
    is_ordered=models.BooleanField(default=False)
    
class ReviewRating(models.Model):
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    user=models.ForeignKey(Account,on_delete=models.CASCADE)
    subject=models.CharField(max_length=100,blank=True)
    review=models.CharField(max_length=500,blank=True)
    rating=models.FloatField()
    ip=models.CharField(max_length=100,blank=True)
    status=models.BooleanField(default=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.subject
    
class Referal(models.Model):
    user=models.OneToOneField(Account,on_delete=models.CASCADE)
    code=models.CharField(max_length=12,blank=True)
    recommended_by=models.ForeignKey(Account,on_delete=models.CASCADE,blank=True,null=True,related_name='ref_by')
    updated=models.DateTimeField(auto_now_add=True) 
    created=models.DateTimeField(auto_now_add=True,blank=True,null=True) 

    def __str__(self):
        return f"{self.user.username}-{self.code}"


  


class ReferalCoupen(models.Model):
     user=models.ForeignKey(Account,on_delete=models.CASCADE) 
     coupon_code=models.CharField(max_length=12,blank=True)
     discount=models.IntegerField(default=20)   


     def __str__(self):
         return self.coupon_code   

class UserPropic(models.Model):
    user=models.OneToOneField(Account,on_delete=models.CASCADE)
    pro_pic=models.ImageField(upload_to='pro_pics',null=True,blank=True)
    
    def image_url(self):
        try:
            url=self.pro_pic.url 
        except :
            url="https://bootdey.com/img/Content/avatar/avatar7.png"
        return url