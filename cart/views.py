from django.http.response import JsonResponse
from order.models import UserAddress
from django.contrib import messages
from store.models import ProductOffer, ReferalCoupen, coupon,UsedOffer
from django.shortcuts import render,redirect,HttpResponse,get_object_or_404
from store.models import Product
from category.models import Category
from .models import Cart,CartItem
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
import requests
from django.http import HttpResponseRedirect
import json
from datetime import date


def index(request):
    product=Product.objects.all().filter(is_available=True)
   
    # today=date.today()
    # today1 = today.strftime("%Y-%m-%d")
    
    for prod in product:
        print(prod.offer_price)
        if prod.check_status():
            pass
        else:
            prod.offer_price=None
            prod.save(update_fields=['offer_price'])
            
    
    context={
        'pro':product,
    }
    return render(request,'shop/Homepage.html',context)

def _cart_id(request):
    cart =request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart


def add_cart(request,product_id):
    current_user = request.user  
    product = Product.objects.get(id=product_id) #get the product
    if current_user.is_authenticated:
        is_cart_item_exists = CartItem.objects.filter(product=product, user=current_user).exists()
        if is_cart_item_exists:
            cart_item = CartItem.objects.filter(product=product, user=current_user)                                                
        try:
            cart_item= CartItem.objects.get(product= product, user= current_user)
            cart_item.quantity += 1
            cart_item.save()  
        except CartItem.DoesNotExist:
            cart_item = CartItem.objects.create(
                product = product,
                quantity = 1,
                user = current_user 
            )
            cart_item.save()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    else:
        try:
            cart = Cart.objects.get(cart_id= _cart_id(request))
        except Cart.DoesNotExist:
            cart = Cart.objects.create(cart_id= _cart_id(request))
        cart.save()
        try:
            cart_item= CartItem.objects.get(product= product, cart= cart)
            cart_item.quantity += 1
            cart_item.save()

        except CartItem.DoesNotExist:
            cart_item = CartItem.objects.create(
                product = product,
                quantity = 1,
                cart = cart
            )
            cart_item.save()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


# Create your views here.





def carts(request, total=0, quantity=0, cart_items=None):
    grand_total = 0
    delivery_chrg = 0
    coupon_rate=0
  
    try:        
        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(user=request.user, is_active=True)
        else:            
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        for cart_item in cart_items:
            if cart_item.product.offer_price == None:
                total+=(cart_item.product.price * cart_item.quantity)
            else:
                total= total+(cart_item.product.offer_price * cart_item.quantity)
        if request.session.get('session_coupon_code'):
            del request.session['session_coupon_code']
           
            
    
        if request.POST.get('coupon_code1'):
            coupon_code=request.POST.get('coupon_code1')
            user=request.user

            if coupon.objects.filter(coupon_code=coupon_code).exists():
                coupon_instance=coupon.objects.get(coupon_code=coupon_code)
                
                
                if UsedOffer.objects.filter(coupon=coupon_instance,user=user,is_ordered=True).exists():
                    return JsonResponse({'status':True,'message':"Coupon Already Used"})
                    
                if coupon_instance.check_expired()==True:
                    request.session["session_coupon_code"]=coupon_code
                    coupon_rate=coupon_instance.coupon_rate
                    delivery_chrg = 100
                    net_total = total+delivery_chrg
                    coupon_offer=net_total*coupon_rate/100
                    grand_total = net_total-coupon_offer 
                    grand="₹ "+str(grand_total)
                    coupon_of="₹ "+str(coupon_offer)
                    return JsonResponse ({'status':True,'message':"Coupon Applied Successfully",'grand_total':grand,'coupon_offer': coupon_of})
               
                
                else:
                    if UsedOffer.objects.filter(user=user,coupon=coupon_instance).exists():
                        pass
                    else:
                        used=UsedOffer(user=user,coupon=coupon_instance)
                        used.save()
                    # used.user=user
                    # used.coupon=coupon1
                    
                    # user1=coupon_code
                
            
            if ReferalCoupen.objects.filter(coupon_code=coupon_code,user=request.user):
                coupon_refer_instance=ReferalCoupen.objects.get(coupon_code=coupon_code,user=request.user)
                coupon_code1=coupon_refer_instance.coupon_code
                coupon_rate=coupon_refer_instance.discount
                
                request.session["session_coupon_code"]=coupon_code1
                delivery_chrg = 100
                net_total = total+delivery_chrg
                coupon_offer=net_total*coupon_rate/100
                grand_total = net_total-coupon_offer 
                grand="₹ "+str(grand_total)
                coupon_of="₹ "+str(coupon_offer)
                return JsonResponse ({'status':True,'message':"Referal Coupon Applied Successfully",'grand_total':grand,'coupon_offer': coupon_of})
           
            else:
                coupon_rate=0
                delivery_chrg = 100
                net_total = total+delivery_chrg
                coupon_offer=net_total*coupon_rate/100
                grand_total = net_total-coupon_offer
                return JsonResponse({'status':True,'message':"Invalid Coupon",'grand_total':grand_total,'coupon_offer': coupon_offer})
        # else:
        #     coupon_rate=0
      
     
        
        delivery_chrg = 100
        net_total = total+delivery_chrg
        coupon_offer=net_total*coupon_rate/100
        grand_total = net_total-coupon_offer
        
    except ObjectDoesNotExist:
        pass
    
    context = {
        'total' : total,
        'quantity' : quantity,
        'cart_items' : cart_items,
        'delivery_chrg' : delivery_chrg,
        'grand_total' : grand_total,
        'coupon_offer': coupon_offer,
        
    }
    return render(request,'shop/cart.html', context)



def remove_cart(request, product_id):
    # cart = Cart.objects.get(cart_id=_cart_id(request))
    # product = get_object_or_404(Product, id=product_id)
    # cart_item = CartItem.objects.get(product=product, cart=cart)
    # if cart_item.quantity > 1:
    #     cart_item.quantity -= 1
    #     cart_item.save()
    # else:
    #     cart_item.delete()
    # return redirect('carts')
    product=get_object_or_404(Product,id=product_id)
    try:
        if request.user.is_authenticated:

           cart_item=CartItem.objects.get(product=product,user=request.user)
        else:  
           cart=Cart.objects.get(cart_id=_cart_id(request)) 
           cart_item=CartItem.objects.get(product=product,cart=cart)
        if cart_item.quantity > 1:
           cart_item.quantity -= 1
           cart_item.save()
        else:
           cart_item.delete()
    except:
        pass       
    return redirect('carts') 


def remove_cart_item(request, product_id):
    # cart = Cart.objects.get(cart_id=_cart_id(request))
    # product = get_object_or_404(Product, id=product_id)
    # cart_item = CartItem.objects.get(product=product, cart=cart)
    # cart_item.delete()
    # return redirect('carts')
    product = get_object_or_404(Product, id = product_id)
    
    if request.user.is_authenticated:
        cart_item = CartItem.objects.get(product = product ,user = request.user)
    else:
        cart = Cart.objects.get(cart_id = _cart_id(request))
        cart_item = CartItem.objects.get(product = product,cart=cart)

    cart_item.delete()
    return redirect('carts') 

@login_required(login_url='login')
def checkout(request, total=0, quantity=0, cart_items=None):
    grand_total = 0
    delivery_chrg = 100
    coupon_rate=0
    coupon_offer=0
    coupon_code=0
    try:
        if request.user.is_authenticated:
            cart_items=CartItem.objects.filter(user=request.user,is_active=True)
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        for cart_item in cart_items:
            if cart_item.product.offer_price == None:
                total+=(cart_item.product.price * cart_item.quantity) 
            else:
                total+=(cart_item.product.offer_price * cart_item.quantity)
                quantity += cart_item.quantity
                
        coupon_co=request.session.get("session_coupon_code")
   
        if coupon.objects.filter(coupon_code=coupon_co).exists():
            coupon_code=coupon.objects.get(coupon_code=coupon_co)
       
        if UsedOffer.objects.filter(coupon=coupon_code,user=request.user,is_ordered=True).exists():
            coupon_rate=0
            
        if ReferalCoupen.objects.filter(coupon_code=coupon_co,user=request.user).exists():
            coupon_refer_instance=ReferalCoupen.objects.get(coupon_code=coupon_co,user=request.user)
            coupon_rate=coupon_refer_instance.discount
        else:
            if coupon.objects.filter(coupon_code=coupon_co).exists():
                coupon_rate=coupon_code.coupon_rate
           
                                
    except ObjectDoesNotExist:
        pass #just ignore
    

    delivery_chrg = 100
    net_total = total+delivery_chrg
    coupon_offer=net_total*coupon_rate/100
    grand_total = net_total-coupon_offer  

    user=request.user
    address=UserAddress.objects.filter(user=user)
    
    context = {
        'total': total,
        'quantity': quantity,
        'cart_items': cart_items,
        'delivery_chrg': delivery_chrg,
        'grand_total': grand_total,
        'address': address,
        'coupon_offer': coupon_offer,
    }
    return render(request, 'shop/checkout.html', context)

def collect_address(request):
    if request.method == "GET":
        id=request.GET['address']
        add=UserAddress.objects.get(id=id)
        print(id)

        data = {}
        data['first_name']=add.first_name
        data['last_name']=add.last_name
        data['phone']=add.phone
        data['email']=add.email
        data['address_line1']=add.address_line1
        data['address_line2']=add.address_line2
        data['city']=add.city
        data['state']=add.state

        return HttpResponse(json.dumps(data), content_type="application/json")

def testcart(request):
    return HttpResponse("success")




