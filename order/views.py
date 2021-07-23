from cart.views import _cart_id
from store.models import UsedOffer, coupon
from django.core.checks import messages
from django.contrib import messages
from django.http.response import HttpResponse,JsonResponse
from django.shortcuts import render
from cart.models import Cart, CartItem
from django.contrib import auth
from django.shortcuts import render,redirect
from .forms import OrderForm,Order
import datetime
from .models import *
from store.models import Product
import json
import razorpay
from .forms import *

# from accounts.models import UserAddress

# Create your views here.
def place_order(request,total=0,quantity=0):
    
    current_user = request.user
    cart_items=CartItem.objects.filter(user=request.user)
    cart_count=cart_items.count()
    if cart_count < 0 :
        return redirect('index')

    grand_total=0
    delivery_chrg=0
    coupon_rate=0
    coupon_code=0
    
 
    # for cart_item in cart_items:
    #     total += (cart_item.product.price * cart_item.quantity)
    #     quantity += cart_item.quantity
    for cart_item in cart_items:
        if cart_item.product.offer_price == None:
            total+=(cart_item.product.price * cart_item.quantity) 
        else:
            total+=(cart_item.product.offer_price * cart_item.quantity) 
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
    
    # if request.session.get("session_coupon_code") == None:
    #     pass
     
    # else:
    #     coupon_co=request.session.get("session_coupon_code")
    #     coupon_code=coupon.objects.get(coupon_code=coupon_co)
        
    #     if UsedOffer.objects.filter(coupon=coupon_code,user=request.user,is_ordered=True).exists():
    #         coupon_rate=0
    #     else:
    #         if coupon.objects.filter(coupon_code=coupon_co).exists():
    #             coupon_rate=coupon_code.coupon_rate
    #         else:
    #             coupon_rate=0
           
    delivery_chrg = 100
    net_total = total+delivery_chrg
    coupon_offer=net_total*coupon_rate/100
    grand_total = net_total-coupon_offer   

    if request.method == 'POST':            
        order=Order()
       
        save_address= request.POST.get('save_address',False)
        if save_address == 'save_address':
            data=request.POST
            user_address=UserAddress()
            if UserAddress.objects.filter(first_name=data['first_name'],last_name=data['last_name'],phone=data['phone'],email=data['email'],address_line1=data['address_line1'],address_line2=data['address_line2'],city=data['city'],state=data['state'],user=request.user.id).exists():
                messages.Info(request,'Address already exist')              
            else:
                user_address.first_name=data['first_name']
                user_address.last_name=data['last_name']
                user_address.phone=data['phone']
                user_address.email=data['email']
                user_address.address_line1=data['address_line1']
                user_address.address_line2=data['address_line2']
                user_address.city=data['city']
                user_address.state=data['state']
                user_address.user=request.user
                user_address.save()              
            
            
        data=request.POST
        
        if Order.objects.filter(user=request.user,is_ordered=False).exists():
            order= Order.objects.get(user=request.user,is_ordered=False)
        else:
            order=Order()

    
        order.first_name=data['first_name']
        order.last_name=data['last_name']
        order.phone=data['phone']
        order.email=data['email']
        order.address_line1=data['address_line1']
        order.address_line2=data['address_line2']
        order.state=data['state']
        order.city=data['city']
        order.order_note=data['order_note']
        order.order_total=grand_total
        order.coupon_offer=coupon_offer
        order.delivery_chrg=delivery_chrg
        order.ip=request.META.get('REMOTE_ADDR')
        order.user=request.user
        order.save()

        #generate order number



        yr=int(datetime.date.today().strftime('%Y'))
        dt=int(datetime.date.today().strftime('%d'))
        mt=int(datetime.date.today().strftime('%m'))
        d=datetime.date(yr,mt,dt)
        current_date=d.strftime("%Y%m%d")  #generate id with based on date
        order_number=current_date+str(order.id)
        
        
        
        
        order.order_number=order_number
        order.save()
        user_details=Order.objects.get(user=current_user,is_ordered=False,order_number=order_number)
        razorpay_total = grand_total*100
        paypal_total = grand_total/74.4
        context={
            'order_user':user_details,
            'cart_items':cart_items,
            'delivery_chrg': delivery_chrg,
            'grand_total':grand_total,
            'razorpay_total': razorpay_total,
            'paypal_total': paypal_total,
            'coupon_offer': coupon_offer,
                      
        }
        return render(request,'shop/payment_choose.html',context)

        # address=UserAddress(user=request.user,first_name=data['firstname'],last_name=data['lastname'],phone=data['phonenumber'],email=data['email'],address_line1=data['address1'],address_line2=data['address2'],city=data['city'],state=data['state'])
        # address.save()
        
    #     request.session['order_id']=order_number
    #     global val
    #     def val():
    #         return order_number
    #     return redirect('payments')
    
    # else:
    return redirect('index')

def confirmation(request):
    return render(request,'shop/confirmation.html')

def payments(request,order_id):
    sub_total=0
    coupon_code=0
    
    if Order.objects.filter(user=request.user,is_ordered=False,order_number=order_id).exists():
        order_data=Order.objects.get(user=request.user,is_ordered=False,order_number=order_id)
        cart_items=CartItem.objects.filter(user=request.user)
    
    coupon_co=request.session.get("session_coupon_code")
   
    if coupon.objects.filter(coupon_code=coupon_co).exists():
        coupon_code=coupon.objects.get(coupon_code=coupon_co)
          
    if UsedOffer.objects.filter(coupon=coupon_code,user=request.user,is_ordered=True).exists():
        pass
    if UsedOffer.objects.filter(coupon=coupon_code,user=request.user,is_ordered=False).exists():
        used=UsedOffer.objects.get(coupon=coupon_code,user=request.user,is_ordered=False)
        used.is_ordered=True
        used.save()
    if ReferalCoupen.objects.filter(coupon_code=coupon_co,user=request.user).exists():
        coupon_refer_instance=ReferalCoupen.objects.get(coupon_code=coupon_co,user=request.user)
        coupon_refer_instance.delete()
    else:
        pass
    
        
    if request.method== 'POST':        
        pay='cod'
        orders_data=Order.objects.get(order_number=order_id) 
        if pay== "cod":
            payment=Payment(user=request.user,payment_id=order_id,payment_method=pay,satus="completed",amount_paid=order_data.order_total)
            payment.save()
            order_data.payment=payment
            order_data.is_ordered=True
            order_data.save()

            for item in cart_items:
                orderproduct=OrderProduct()
                orderproduct.order=order_data
                orderproduct.user=request.user
                orderproduct.payment=payment
                orderproduct.product=item.product
                orderproduct.quantity=item.quantity                
                orderproduct.product_price=item.product.price 
                
                orderproduct.ordered=True
                orderproduct.save()
                # if item.product.offer_price == None:
                #     sub_total+=item.product.product_price*item.quantity
                # else:
                #     sub_total+=item.product.offer_price*item.quantity
                    

                #reduce the quantity

                product1=Product.objects.get(id=item.product_id)
                
                product1.stock -= item.quantity
                product1.save()
                cart_items.delete()

            # CartItem.objects.filter(user=request.user).delete()
            # cart1 =request.session.session_key 
            # cart = Cart.objects.get(cart_id=cart1)
            # cart_items = CartItem.objects.filter(cart=cart, is_active=True)
            # cart_prod=CartItem.objects.filter(user=request.user)    
            # print(cart_prod.product.id,"dddddddddddddddddddd")      
          
              
            order=OrderProduct.objects.filter(order=orders_data) 
            # sub_total=0
           
          
          
            coupon_offer=orders_data.coupon_offer
            grand_total = orders_data.order_total
                        
            
            
            
            
            # if order.product.offer_price == None
            # for pro in order:
            #     sub_total+=pro.product_price*pro.quantity
            
            
             
            context={
                'orders':order,
                'orders_data':orders_data,
                'sub_total': sub_total,
                'coupon_offer': coupon_offer,
                'grand_total': grand_total,
                
                }
            
           
            return render(request,'shop/invoice.html',context)
def payment_method_paypal(request):
    body=json.loads(request.body)
    order=Order.objects.get(user=request.user,is_ordered=False,order_number=body['orderID'])
    payment=Payment(
        user=request.user,
        payment_id=body['trans_ID'],
        payment_method=body['payment_method'],
        amount_paid=order.order_total,
        satus=body['status'])
    payment.save()
    order.payment=payment
    order.is_ordered=True
    order.save()
    

    cart_items=CartItem.objects.filter(user=request.user)
    for item in cart_items:
        orderproduct=OrderProduct()
        orderproduct.order=order
        orderproduct.user=request.user
        orderproduct.payment=payment
        orderproduct.product=item.product
        orderproduct.quantity=item.quantity    
        orderproduct.product_price=item.product.price       
        orderproduct.ordered=True
        orderproduct.save()
        product=Product.objects.get(id=item.product_id)
        product.stock -= item.quantity
        product.save()
    cart_prod=CartItem.objects.filter(user=request.user)
    cart_prod.delete()
    data={
        'order_number':order.order_number,
        'transID':payment.payment_id
    }   

    return JsonResponse(data)

def payment_complete(request):
    # {'orderID': '20210709151', 'trans_ID': '3CS87553WN617873H', 'payment_method': 'PayPal', 'status': 'COMPLETED'}
    # this is from json respose 'data' dict 
    coupon_code=0
    coupon_co=request.session.get("session_coupon_code")
   
    if coupon.objects.filter(coupon_code=coupon_co).exists():
        coupon_code=coupon.objects.get(coupon_code=coupon_co)
          
    if UsedOffer.objects.filter(coupon=coupon_code,user=request.user,is_ordered=True).exists():
        pass
    if UsedOffer.objects.filter(coupon=coupon_code,user=request.user,is_ordered=False).exists():
        used=UsedOffer.objects.get(coupon=coupon_code,user=request.user,is_ordered=False)
        used.is_ordered=True
        used.save()
    if ReferalCoupen.objects.filter(coupon_code=coupon_co,user=request.user).exists():
        coupon_refer_instance=ReferalCoupen.objects.get(coupon_code=coupon_co,user=request.user)
        coupon_refer_instance.delete()
    else:
        pass
    
    
    
    
    order_number=request.GET.get('order_number')
    trans_id=request.GET.get('payment_id')

    

    try:
        order=Order.objects.get(order_number=order_number,is_ordered=True)
        order_produuct=OrderProduct.objects.filter(order_id=order.id)
        payment=Payment.objects.get(payment_id=trans_id)
        context={
            'order':order,
            'order_product':order_produuct,
            'order_number':order.order_number,
            'payment':payment
        }
        
        
        return render(request,'shop/confirmation.html',context)
    except (Payment.DoesNotExist,Order.DoesNotExist):
        return redirect('index')
    
    
def razor_pay(request):
    coupon_code=0
    coupon_co=request.session.get("session_coupon_code")
   
    if coupon.objects.filter(coupon_code=coupon_co).exists():
        coupon_code=coupon.objects.get(coupon_code=coupon_co)
          
    if UsedOffer.objects.filter(coupon=coupon_code,user=request.user,is_ordered=True).exists():
        pass
    if UsedOffer.objects.filter(coupon=coupon_code,user=request.user,is_ordered=False).exists():
        used=UsedOffer.objects.get(coupon=coupon_code,user=request.user,is_ordered=False)
        used.is_ordered=True
        used.save()
    if ReferalCoupen.objects.filter(coupon_code=coupon_co,user=request.user).exists():
        coupon_refer_instance=ReferalCoupen.objects.get(coupon_code=coupon_co,user=request.user)
        coupon_refer_instance.delete()
    else:
        pass
    if request.method=='POST':
        order_id=request.POST.get('order_id')
        order=Order.objects.get(user=request.user,order_number=order_id,is_ordered=False)
        payment=Payment(user=request.user,payment_id=order_id,payment_method='razorpay',amount_paid=order.order_total,satus='completed')
        payment.save()
        order.payment=payment
        order.is_ordered=True
        order.save()
        cart_items=CartItem.objects.filter(user=request.user)


        for items in cart_items:

            order_product = OrderProduct()
            order_product.order=order
            order_product.payment=payment
            order_product.user=request.user
            order_product.quantity=items.quantity
            order_product.product_price=items.product.price
            order_product.product=items.product
    
            order_product.ordered=True
            order_product.status='Accepted'
            order_product.save()


            product=Product.objects.get(id=items.product_id)
            product.stock -= product.stock-items.quantity
            product.save()
        cart_items=CartItem.objects.filter(user=request.user)
        cart_items.delete()
       

        order=Order.objects.get(order_number=order_id,is_ordered=True)
        order_produuct=OrderProduct.objects.filter(order_id=order.id)
        address=UserAddress.objects.filter(user=request.user)
        context={

                'order': order,
                'order_product': order_produuct,
                'order_number': order.order_number,
                'payment':payment,
                'address':address
            
            }
        return render(request,'shop/confirmation.html',context)
    
    
    
def invoice(request,order_id):   
    orders_data=Order.objects.get(order_number=order_id)    
    order=OrderProduct.objects.filter(order=orders_data)   
    context={
        'orders':order,
        'orders_data':orders_data,
        }
    return render(request,'shop/invoice.html',context) 
        
def submit_review(request, product_id):
    url = request.META.get('HTTP_REFERER')
    if request.method == 'POST':
        try:
            reviews = ReviewRating.objects.get(user__id=request.user.id, product__id=product_id)
            form = ReviewForm(request.POST, instance=reviews)
            form.save()
            messages.success(request, 'Thank you! Your review has been updated.')
            return redirect(url)
        except ReviewRating.DoesNotExist:
            form = ReviewForm(request.POST)
            if form.is_valid():
                data = ReviewRating()
                data.subject = form.cleaned_data['subject']
                data.rating = form.cleaned_data['rating']
                data.review = form.cleaned_data['review']
                data.ip = request.META.get('REMOTE_ADDR')
                data.product_id = product_id
                data.user_id = request.user.id
                data.save()
                messages.success(request, 'Thank you! Your review has been submitted.')
                return redirect(url)