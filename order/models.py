from django.db import models
from accounts.models import *

from store.models import *

# Create your models here.


class Payment(models.Model):
    user=models.ForeignKey(Account,on_delete=models.CASCADE)
    payment_id=models.CharField(max_length=100,blank=True)
    payment_method=models.CharField(max_length=100)
    amount_paid=models.FloatField(null=True)
    satus=models.CharField(max_length=100)
    created_at=models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.payment_id





class Order(models.Model):

    
    STATUS =(
        ('New','New'),
        ('Accepted','Accepted'),
        ('Shipped','Shipped'),
        ('Completed','Completed'),
        ('Cancelled','Cancelled')
    ) 

          

    user=models.ForeignKey(Account,on_delete=models.SET_NULL,null=True)
    payment=models.ForeignKey(Payment,on_delete=models.SET_NULL,blank=True,null=True)
    order_number=models.CharField(max_length=100,null=True)
    first_name=models.CharField(max_length=50)
    last_name=models.CharField(max_length=50)
    phone=models.CharField(max_length=50)
    email=models.EmailField(max_length=50)
    address_line1=models.CharField(max_length=50)
    address_line2=models.CharField(max_length=50,blank=True)
    
    city=models.CharField(max_length=50)
    state=models.CharField(max_length=50)
    order_note=models.CharField(max_length=100,blank=True)
    order_total=models.FloatField(null=True)
    coupon_offer=models.FloatField(null=True)
    delivery_chrg=models.FloatField(null=True)
    status=models.CharField(max_length=30,choices=STATUS,default='New')
    ip=models.CharField(max_length=100,blank=True)
    is_ordered=models.BooleanField(default=False)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)



    def __str__(self):
        return self.first_name

    def full_name(self):
        return f'{self.first_name} {self.last_name}'  

    def full_address(self):
        return f'{self.address_line1} {self.address_line2}'      


class OrderProduct(models.Model):
    order=models.ForeignKey(Order,on_delete=models.CASCADE)
    payment=models.ForeignKey(Payment,on_delete=models.SET_NULL,blank=True,null=True)
    user=models.ForeignKey(Account,on_delete=models.CASCADE)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity=models.IntegerField()
    product_price=models.FloatField()
    ordered=models.BooleanField(default=False)
    status=models.CharField(default='Pending',max_length=20,null=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    user_cancelled=models.CharField(default=False,max_length=20,null=True)
    

    def __str__(self):
        return self.product.product_name
            
class UserAddress(models.Model):
    user=models.ForeignKey(Account,on_delete=models.CASCADE)  
    first_name=models.CharField(max_length=50)
    last_name=models.CharField(max_length=50)
    phone=models.CharField(max_length=50)
    email=models.EmailField(max_length=50)
    address_line1=models.CharField(max_length=50)
    address_line2=models.CharField(max_length=50,blank=True)
    
    city=models.CharField(max_length=50)
    state=models.CharField(max_length=50)  


    def __str__(self):
        return self.first_name
    

