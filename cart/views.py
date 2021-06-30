from django.shortcuts import render
from store.models import Product
from category.models import Category



# Create your views here.
def index(request):
    product=Product.objects.all().filter(is_available=True)
    context={
        'pro':product,
    }
    return render(request,'shop/Homepage.html',context)


