
from django.db import models
from store.models import Product
from accounts.models import Account
from store.models import CategoryOffer,ProductOffer

# Create your models here.

class Cart(models.Model):
    cart_id = models.CharField(max_length=250, blank=True)
    date_add = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.cart_id


class CartItem(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    cart    = models.ForeignKey(Cart, on_delete=models.CASCADE, null=True)
    quantity = models.IntegerField()
    is_active = models.BooleanField(default=True)

    def sub_total(self):
        
        if self.product.offer_price == None:
            return (self.product.price) * (self.quantity)
        else:
            return int(self.product.offer_price)* (self.quantity)

    def __unicode__(self):
        return self.product


