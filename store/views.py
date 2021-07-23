from store.models import CategoryOffer, ReviewRating
from order.models import Order, OrderProduct
from category.models import Category
from django.shortcuts import render, get_object_or_404
from store.models import Product
from cart.models import CartItem
from django.core.paginator import EmptyPage,PageNotAnInteger,Paginator


from cart.views import _cart_id

# Create your views here.


def store(request,category_slug=None):
    categories = None
    products = None
    if category_slug != None:
        categories = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.filter(category=categories, is_available=True)
        for prod in products:
            if prod.check_status():
                pass
            else:
                prod.offer_price=None
                prod.save(update_fields=['offer_price'])
        paginator=Paginator(products,2)
        page=request.GET.get('page')
        paged_products=paginator.get_page(page)
        product_count = products.count()
    else:   
        products=Product.objects.all().filter(is_available=True)
        for prod in products:
            if prod.check_status():
                pass
            else:
                prod.offer_price=None
                prod.save(update_fields=['offer_price'])
        paginator=Paginator(products,2)
        page=request.GET.get('page')
        paged_products=paginator.get_page(page)
        product_count = products.count()
        
    context ={
        'pro':paged_products,
        'product_count':product_count,
    }
    return render(request,'shop/store.html',context)


def product_detail(request,category_slug,product_slug):
    try:
        single_product = Product.objects.get(category__slug=category_slug,slug=product_slug)
        in_cart = CartItem.objects.filter(cart__cart_id=_cart_id(request), product=single_product).exists()
    except Exception as e:
        raise e
    review = ReviewRating.objects.filter(product_id=single_product.id, status=True)
    context = {
        'single_product': single_product,
        'in_cart'       : in_cart,
        'review'        : review,
      
    }
    return render(request,'shop/productdetails.html',context)
    